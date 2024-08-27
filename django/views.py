from allauth.socialaccount.models import SocialLogin
from allauth.socialaccount.providers.oauth2.views import OAuth2View

from django.conf import settings
from ihela_client.client import Client as iHelaAPIClient

# from allauth.socialaccount.providers.oauth2.client import OAuth2Client, OAuth2Error
# from ihelaprovider.base import iHelaAdapter


TEST_ENV = False


class iHelaClientBaseView(OAuth2View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)

        self.provider = self.adapter.get_provider()
        self.app = self.provider.get_app(self.request)
        self.client = self.get_client(request, self.app)
        self.client.state = SocialLogin.stash_state(request)

        if request.method == "GET":
            return self.get(request, *args, **kwargs)
        elif request.method == "POST":
            return self.post(request, *args, **kwargs)
        else:
            pass
            # Raise Method Not Allowed

    def get_client(self):
        cl = iHelaAPIClient(
            self.client.consumer_key,
            self.client.consumer_secret,
            state=self.client.state,
            test=TEST_ENV,
            ihela_url=settings.OAUTH_IHELA_SERVER_BASEURL + "/",
        )

        return cl

    @property
    def get_absolute_url(self):
        return self.request.build_absolute_uri(self.request.path)


class iHelaClientCodeView(iHelaClientBaseView):
    def get_code(self):
        return self.request.GET.get("code", None)

    def get_error(self):
        return self.request.GET.get("error", None)

    def get_payment_object(self):
        raise NotImplementedError(
            "An iHelaClientCodeView child must have a method called `get_payment_object`."
        )
