from django.shortcuts import render


def admin_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not (request.user.is_superuser or request.user.is_staff):
            return render(
                request,
                'core/error.html',
                {'error_message': 'Access denied'},
                status=403
            )
        return view_func(request, *args, **kwargs)
    return _wrapped_view
