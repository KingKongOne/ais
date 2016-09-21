from django.db import models


# A company (or organisation) participating in a fair
class Exhibitor(models.Model):
    company = models.ForeignKey('companies.Company')
    fair = models.ForeignKey('fair.Fair')

    def __str__(self):
        return self.company.name


# Work field that an exhibitor operates in
class WorkField(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


# Job type that an exhibitor offers
class JobType(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


# Continent that an exhibitor operates in
class Continent(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


# Value or work environment that an exhibitor has
class Value(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


# Info about an exhibitor to be displayed in apps and on website
class CatalogInfo(models.Model):
    company = models.OneToOneField(Exhibitor, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=64)
    slug = models.SlugField(db_index=False)
    short_description = models.CharField(max_length=64)
    description = models.TextField()
    employees_sweden = models.IntegerField()
    employees_world = models.IntegerField()
    countries = models.IntegerField()
    website_url = models.CharField(max_length=128, blank=True)
    facebook_url = models.CharField(max_length=128, blank=True)
    twitter_url = models.CharField(max_length=128, blank=True)
    linkedin_url = models.CharField(max_length=128, blank=True)

    # TODO logo
    # TODO ad

    programs = models.ManyToManyField('people.Programme', blank=True)
    main_work_field = models.ForeignKey(
        WorkField, blank=True, related_name='+')
    work_fields = models.ManyToManyField(
        WorkField, blank=True, related_name='+')
    job_types = models.ManyToManyField(JobType, blank=True)

    def __str__(self):
        return self.display_name
