from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin


class LoginCheckMiddleWare(MiddlewareMixin):

    def process_view(self, request, view_func, view_args, view_kwargs):
        modulename = view_func.__module__
        print(modulename)
        user = request.user
        if user.is_authenticated:

            if user.user_type == "1":
                if modulename == "home.AdminViews":
                    pass
                elif modulename == "home.views" or modulename == "django.views.static":
                    pass
                elif modulename == "django.contrib.auth.views" or modulename == "django.contrib.admin.sites":
                    pass
                else:
                    return HttpResponseRedirect(reverse("home:admin_home"))

            elif user.user_type == "2":
                if modulename == "home.DoctorViews":
                    pass
                elif modulename == "home.views" or modulename == "django.views.static":
                    pass
                elif modulename == "predict_heart.views":
                    pass
                elif modulename == "predict_kidney.views":
                    pass
                elif modulename == "predict_cancers.views":
                    pass
                elif modulename == "predict_diabetes.views":
                    pass
                else:
                    return HttpResponseRedirect(reverse("home:doctor_home"))

            else:
                return HttpResponseRedirect(reverse("home:show_login"))

        else:
            if request.path == reverse("home:show_login") or request.path == reverse("home:do_login") or modulename == "django.contrib.auth.views" or modulename == "django.contrib.admin.sites":
                pass
            else:
                return HttpResponseRedirect(reverse("home:show_login"))
