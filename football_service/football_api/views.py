from django.views.generic import TemplateView


class OpenAPISchemaView(TemplateView):
    template_name = "openapi.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        schema_url = self.kwargs.get("schema_api")  # Get the value from the URL path
        context["extra_context"] = {"schema_api": schema_url}
        return context
