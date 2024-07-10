from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Departments"


class Project(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Projects"


class Category(models.Model):
    date_created = models.DateTimeField(auto_now=True, blank=True, null=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'category list'

    def __str__(self):
        return str({self.name})


class Budget_Management(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    date_created = models.DateTimeField(auto_now=True, blank=True, null=True)
    department = models.ForeignKey(
        Department, on_delete=models.SET_NULL, blank=True, null=True
    )
    project = models.ForeignKey(
        Project, on_delete=models.SET_NULL, blank=True, null=True
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True
    )
    remarks = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = 'budget management'

    def __str__(self):
        return str(self.id)


class Expense_Management(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    date_created = models.DateTimeField(auto_now=True, blank=True, null=True)
    department = models.ForeignKey(
        Department, on_delete=models.SET_NULL, blank=True, null=True
    )
    project = models.ForeignKey(
        Project, on_delete=models.SET_NULL, blank=True, null=True
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    remarks = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Expense_Management'

    def __str__(self):
        return str(self.name)
