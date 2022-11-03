'''
Created on 29 Feb 2016

@author: achickermane
'''
from bgsite.models import Image
from dataentry.models import Table, Template
import json

def get_column_names():
    """"
    Returns a list of (column_id, column_values) for the form
    to use as choices for the column field when creating/editing
    columns
    """
    column_names = []
    for table in Table.objects.all():
        columns = table.get_all_columns()
        for column in columns:
            if not column.is_compulsary:
                value_dict = column.column_values()
                column_names.append((str(column.id), json.dumps(value_dict)))
    return column_names

def get_base_templates():
    templates = []
    for template in Template.objects.all():
        templates.append((template.id,template.name))
    return templates
        

def get_burial_images():
    burial_images_by_book = {}
    # _t_ signifies title page, _u_ signifies end pages, exclude those
    for burial_image in Image.objects.exclude(url__icontains='_t_').exclude(url__icontains='_u_').filter(url__regex=r'[A-Za-z0-9]+_[0-9\-]+_[0-9]+\.jpg').filter(image_type__image_type='burial_record'):
        name_split = str.split(burial_image.url.name, '_')
        if len(name_split) > 0:
            burial_book = name_split[len(name_split)-2]
            if burial_book not in burial_images_by_book:
                url = burial_image.url.url
                extent = [0,0,burial_image.url.width, burial_image.url.height]
                has_template = Template.objects.filter(book_name=burial_book).exists()
                burial_images_by_book[burial_book] = json.dumps({'url':url, 'extent':extent, 'book_name':burial_book, 'has_template': has_template})
    burial_images_by_book = list(burial_images_by_book.items())
    burial_images_by_book.sort(reverse=True)
    return burial_images_by_book


def get_burial_books():
    burial_images_by_book = {}
    # _t_ signifies title page, _u_ signifies end pages, exclude those
    for burial_image in Image.objects.exclude(url__icontains='_t_').exclude(url__icontains='_u_').filter(url__regex=r'[A-Za-z0-9]+_[0-9\-]+_[0-9]+\.jpg').filter(image_type__image_type='burial_record'):
        name_split = str.split(burial_image.url.name, '_')
        if len(name_split) > 0:
            burial_book = name_split[len(name_split)-2]
            url = burial_image.url.url
            burial_images_by_book[burial_book] = burial_book
    return burial_images_by_book.items()


def get_templates():
    """
    Returns all templates
    """
    templates = []
    for template in Template.objects.all():
        value_dict = {}
        value_dict['id'] = str(template.id)
        value_dict['name'] = template.name
        value_dict['bookName'] = template.book_name
        value = (template.id, json.dumps(value_dict))
        templates.append(value)
    return templates
