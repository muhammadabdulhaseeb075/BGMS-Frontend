DELETE FROM barton.django_content_type;
insert into barton.django_content_type select *  from public.django_content_type;

DELETE FROM caldbeck.django_admin_log;
DELETE FROM caldbeck.django_content_type;
insert into caldbeck.django_content_type select *  from public.django_content_type;

DELETE FROM dalstondemo.django_content_type;
insert into dalstondemo.django_content_type select *  from public.django_content_type;

DELETE FROM dalston.django_content_type;
insert into dalston.django_content_type select *  from public.django_content_type;

DELETE FROM dalton.django_content_type;
insert into dalton.django_content_type select *  from public.django_content_type;

DELETE FROM finsthwaite.django_content_type;
insert into finsthwaite.django_content_type select *  from public.django_content_type;

DELETE FROM martindale.django_content_type;
insert into martindale.django_content_type select *  from public.django_content_type;

DELETE FROM watermillock.django_content_type;
insert into watermillock.django_content_type select *  from public.django_content_type;

DELETE FROM wigtonnts.django_content_type;
insert into wigtonnts.django_content_type select *  from public.django_content_type;
