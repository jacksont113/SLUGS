from django.views.generic.base import TemplateView


# Create your views here.
def merge_dicts(x, y):
    """
    Given two dicts, merge them into a new dict as a shallow copy.
    """
    z = x.copy()
    z.update(y)
    return z


class MultipleFormView(TemplateView):
    """
    View mixin that handles multiple forms / formsets.
    After the successful data is inserted ``self.process_forms`` is called.
    """

    form_classes = {}
    form_instances = {}

    def get_context_data(self, **kwargs):
        context = super(MultipleFormView, self).get_context_data(**kwargs)
        forms_initialized = {}
        for name, obj in self.form_classes.items():
            if "instance" in obj:
                forms_initialized[name] = obj["form"](
                    obj["args"] if "args" in obj else None,
                    prefix=name,
                    instance=obj["instance"],
                )
            else:
                forms_initialized[name] = obj["form"](
                    obj["args"] if "args" in obj else None,
                    prefix=name,
                )

        return merge_dicts(context, forms_initialized)

    def post(self, request, **kwargs):
        forms_initialized = {}
        for name, obj in self.form_classes.items():
            if "args" in obj:
                forms_initialized[name] = obj["form"](
                    obj["args"], prefix=name, data=request.POST
                )
            else:
                forms_initialized[name] = obj["form"](prefix=name, data=request.POST)
            if "instance" in obj:
                forms_initialized[name].instance = obj["instance"]

        valid = all(
            [form_class.is_valid() for form_class in forms_initialized.values()]
        )
        if valid:
            return self.process_forms(forms_initialized)
        else:
            context = merge_dicts(self.get_context_data(), forms_initialized)
            return self.render_to_response(context)

    def process_forms(self, form_instances):
        raise NotImplementedError
