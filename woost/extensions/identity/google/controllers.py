#-*- coding: utf-8 -*-
"""

.. moduleauthor:: Pepe Osca <pepe.osca@whads.com>
"""
import cherrypy
from oauth2client.client import OAuth2WebServerFlow
import httplib2
from googleapiclient import discovery
from cocktail.styled import styled
from cocktail.controllers import (
    Controller,
    session,
    redirect,
    get_request_root_url_builder
)
from woost import app
from woost.controllers.cmscontroller import CMSController

from .identityprovider import GoogleIdentityProvider

SESSION_PREFIX = "woost.extensions.identity.google."


class GoogleOAuthController(Controller):

    def resolve(self, path):

        if not path:
            raise cherrypy.HTTPError(400)

        provider_id = path[0]

        try:
            provider_id = int(provider_id)
        except ValueError:
            raise cherrypy.HTTPError(400)

        provider = GoogleIdentityProvider.get_instance(provider_id)
        if provider is None:
            raise cherrypy.NotFound()

        path.pop(0)
        return GoogleOAuthProviderController(provider)


class GoogleOAuthProviderController(Controller):

    def __init__(self, provider):
        Controller.__init__(self)
        self.provider = provider
        self.target_url = (
            session.get(SESSION_PREFIX + "target_url")
            or app.website.home.get_uri()
        )

    def step_url(self, step_number):
        url_builder = get_request_root_url_builder()
        url_builder.path = [
            "google_oauth",
            self.provider.id,
            "step%d" % step_number
        ]
        return url_builder.get_url()

    @cherrypy.expose
    def step1(self, code = None, target_url = None, **kwargs):

        if target_url:
            self.target_url = target_url
            session[SESSION_PREFIX + "target_url"] = target_url

        flow = OAuth2WebServerFlow(
            self.provider.client_id,
            self.provider.client_secret,
            self.provider.scope,
            redirect_uri = self.step_url(1)
        )
        flow.params["access_type"] = self.provider.access_type

        if not code:
            redirect(flow.step1_get_authorize_url())

        if self.provider.debug_mode:
            print(styled("Google authorization code:", "magenta"), code)

        credentials = flow.step2_exchange(code)
        session[SESSION_PREFIX + "credentials"] = credentials

        if self.provider.debug_mode:
            print(styled("Google refresh token:", "magenta"), end=' ')
            print(credentials.refresh_token)
            print(styled("Google access token:", "magenta"), end=' ')
            print(credentials.access_token)

        redirect(self.step_url(2))

    @cherrypy.expose
    def step2(self):

        credentials = session.get(SESSION_PREFIX + "credentials")

        if not credentials or credentials.access_token_expired:
            redirect(self.step_url(1))

        http_auth = credentials.authorize(httplib2.Http())
        oauth2_service = discovery.build('oauth2', 'v2', http_auth)
        user_data = oauth2_service.userinfo().get().execute()

        if self.provider.debug_mode:
            print(styled("Google user profile:", "magenta"), user_data)

        self.provider.login(user_data)
        del session[SESSION_PREFIX + "credentials"]

        redirect(self.target_url)

    @cherrypy.expose
    def refresh_token(self, code):
        response = self.provider.get_refresh_token(code)
        return (
            """
            <input id="code" type="text" autofocus value="%s">
            <script type="text/javascript">
                window.onload = function () {
                    document.getElementById("code").select();
                }
            </script>
            """
            % response["refresh_token"]
        )


CMSController.google_oauth = GoogleOAuthController

