from django_unicorn.components import UnicornView
from gig.models import Gig, JobInterest, Job, DEPARTMENTS
from employee.models import Employee
from SLUGS.templatetags.grouping import has_group

class GigsignupView(UnicornView):
    jobs = {}
    all_jobs = {}
    user_id = None
    gig_id = None

    def setJobs(self):
        gig = Gig.objects.get(pk=self.gig_id)
        user = Employee.objects.get(pk=self.user_id)
        # Jobs that they can sign up for
        for job in gig.job_set.filter(
            employee=None, position__in=user.groups.all()
        ).order_by("department"):
            self.jobs[str(job.pk)] = (
                job,
                JobInterest.objects.filter(employee=user, job=job).first(),
                True
            )
        # Jobs they can test for
        depts = []
        for dept in DEPARTMENTS:
            if has_group(user, dept[1]) and not has_group(user, f'Probie - {dept[1]}'):
                depts.append(dept[0])
        for job in (gig.job_set.filter(
            employee=None, department__in=depts
            )
            .exclude(position__in=user.groups.all())
            .order_by("department")
        ):
            self.jobs[str(job.pk)] = (
                job,
                JobInterest.objects.filter(employee=user, job=job).first(),
                False
            )
        # All jobs
        for job in (
            gig.job_set.filter(employee=None)
            .order_by("department")
        ):
            self.all_jobs[str(job.pk)] = job.position

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self.user_id = kwargs["u_id"]
        self.gig_id = kwargs["gig_id"]
        self.setJobs()

    def toggleInterest(self, job_id):
        job = Job.objects.get(pk=job_id)
        employee = Employee.objects.get(pk=self.user_id)
        is_Signedup = (
            True
            if JobInterest.objects.filter(employee=employee, job=job).first()
            is not None
            else False
        )
        if is_Signedup:
            JobInterest.objects.get(employee=employee, job=job).delete()
        else:
            JobInterest.objects.get_or_create(employee=employee, job=job)
        self.setJobs()
