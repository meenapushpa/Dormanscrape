from django.db import models


# Create your models here.
class fme_cat(models.Model):
    original_part_number = models.CharField(max_length=200)
    part_no = models.CharField(max_length=200)
    manufacturer_name = models.CharField(max_length=200)
    product_type = models.CharField(max_length=200)

    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}, {}, {}, {}".format(self.original_part_number, self.part_no, self.manufacturer_name, self.product_type)


class fme_mx(models.Model):
    original_part_number = models.CharField(max_length=200)
    part_no = models.CharField(max_length=200)
    manufacturer_name = models.CharField(max_length=200)
    product_type = models.CharField(max_length=200)

    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}, {}, {}, {}".format(self.original_part_number, self.part_no, self.manufacturer_name, self.product_type)


class mevotech(models.Model):
    original_part_number = models.CharField(max_length=200)
    part_no = models.CharField(max_length=200)
    manufacturer_name = models.CharField(max_length=200)
    product_type = models.CharField(max_length=200)

    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}, {}, {}, {}".format(self.original_part_number, self.part_no, self.manufacturer_name, self.product_type)


class nexcat(models.Model):
    original_part_number = models.CharField(max_length=200)
    oe_part_no = models.CharField(max_length=200)
    am_part_no = models.CharField(max_length=200)
    manufacturer_name = models.CharField(max_length=200)

    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}, {}, {}, {}".format(self.original_part_number, self.oe_part_no, self.am_part_no, self.manufacturer_name)


class nexcat_new(models.Model):
    part_number = models.CharField(max_length=200)
    brand = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    manufacturer = models.CharField(max_length=200)
    am_part_no = models.CharField(max_length=200)


    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}, {}, {}, {}".format(self.part_number, self.brand, self.title, self.manufacturer, self.am_part_no)

class dorman(models.Model):
    original_part_number = models.CharField(max_length=200)
    product_name = models.CharField(max_length=200)
    product_info = models.CharField(max_length=200)
    application_summary = models.CharField(max_length=200)
    cross = models.CharField(max_length=200)
    part_no = models.CharField(max_length=200)
    manufacturer_name = models.CharField(max_length=200)

    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}, {}, {}, {}, {}, {}, {}".format(self.original_part_number, self.product_name, self.product_info, self.application_summary, self.cross, self.part_no, self.manufacturer_name)


class trw(models.Model):
    year = models.CharField(max_length=200)
    make = models.CharField(max_length=200)
    model = models.CharField(max_length=200)
    product = models.CharField(max_length=200)
    part_number = models.CharField(max_length=200)
    part_type = models.CharField(max_length=200)
    application = models.CharField(max_length=200)

    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}, {}, {}, {}, {}, {}, {}".format(self.year, self.make, self.model, self.product, self.part_number, self.part_type, self.application)
