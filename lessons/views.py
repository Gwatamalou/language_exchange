from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView



class ConferenceView(LoginRequiredMixin, TemplateView):
    template_name = 'lessons/conference.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'room_name': self.kwargs['room'],  # Получаем значение room из URL
            'auth': self.request.user.id,
            'user_name': self.request.user.username
        })
        return context

