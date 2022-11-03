from django.shortcuts import render_to_response


def csrf_failure(request, reason=""):
    ctx = {'message': 'csrf error'}
    return render_to_response('403_csrf.html', ctx, status=403)