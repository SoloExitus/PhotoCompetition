from django.views.generic.base import TemplateView

from rest_framework.permissions import IsAuthenticated

from competition.forms import PostForm

from competition.models import PhotoPost

from competition.serializers.PhotoPost import PhotoPostDetailSerializer


class HomePageView(TemplateView):
    template_name = "competition/gallery.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pageTitle'] = 'Competition Gallery'
        return context


class PostDetailView(TemplateView):
    template_name = "competition/post_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pageTitle'] = 'Competition Post'
        return context


class ProfileView(TemplateView):
    template_name = "competition/profile.html"
    permission_classes = [IsAuthenticated]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pageTitle'] = 'Competition Profile'
        return context


class PhotoPostCreateView(TemplateView):
    template_name = "competition/photopostcreate.html"
    permission_classes = [ IsAuthenticated, ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pageTitle'] = 'Create Post'
        context['form'] = PostForm()
        return context


class PhotoPostEditView(TemplateView):
    template_name = "competition/photopostedit.html"
    permission_classes = [ IsAuthenticated ]

    def get_context_data(self, **kwargs):
        import pdb
        #pdb.set_trace()

        pk = kwargs['pk']

        post = PhotoPost.objects.get(id=pk)

        context = super().get_context_data(**kwargs)
        context['pageTitle'] = 'Edit Post'
        context['form'] = PostForm(instance=post)
        return context
