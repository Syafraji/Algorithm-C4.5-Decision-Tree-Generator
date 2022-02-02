use project

create table dbo.[REF_HOBI](
Hobi_id bigint primary key identity,
Hobi varchar(50),
)

Create Table dbo.[KRITERIA] (
kriteria_id bigint primary key identity ,
Buta_Warna bit,
Hobi_id bigint foreign key (Hobi_id) references [REF_HOBI](Hobi_id),
Matematika Int,
Pkn int,
Tik int,
Fisika Int,
Biologi Int,
Kimia Int--,
--B_Indonesia Int,
--B_Inggris Int
)

Create Table dbo.[REF_HASIL_FAKULTAS](
hasil_fakultas_id bigint primary key identity,
nama_fakultas varchar(50)
)

create Table dbo.[MAHASISWA](
mahasiswa_id bigint primary key identity ,
first_name varchar(50),
last_name varchar(50),
gender varchar(50),
kriteria_id bigint foreign key (kriteria_id) references kriteria(kriteria_id),
hasil_fakultas_id bigint foreign key (hasil_fakultas_id) references [REF_HASIL_FAKULTAS](hasil_fakultas_id))


Create Table dbo.[USER] (
user_id bigint primary key identity,
username varchar(50),
password varchar(50),
Admin bit,
email varchar(50),
mahasiswa_id bigint foreign key (mahasiswa_id) references mahasiswa(mahasiswa_id)
)

drop table dbo.REF_HOBI
drop table dbo.REF_HASIL_FAKULTAS
drop table dbo.KRITERIA
drop table dbo.[USER]
drop table dbo.MAHASISWA

Delete dbo.ref_hobi
delete dbo.ref_hasil_fakultas
Delete  dbo.KRITERIA
Delete  dbo.[USER]
Delete  dbo.MAHASISWA

Select * from dbo.REF_HOBI
Select * from dbo.REF_HASIL_FAKULTAS
Select * from dbo.KRITERIA
Select * from dbo.[USER]
Select * from dbo.MAHASISWA

insert into dbo.[USER]
values('admin','cGFzc3dvcmQ=',1,null,null),
('wil','cGFzc3dvcmQ=',0,'wil@gmail.com',null),
('wal','cGFzc3dvcmQ=',0,'wal@gmail.com',null),

insert into dbo.[USER]
values('test1','cGFzc3dvcmQ=',0,null,null),
('test2','cGFzc3dvcmQ=',0,null,null),
('test3','cGFzc3dvcmQ=',0,null,null),
('test4','cGFzc3dvcmQ=',0,null,null),
('test5','cGFzc3dvcmQ=',0,null,null),
('test6','cGFzc3dvcmQ=',0,null,null),
('test7','cGFzc3dvcmQ=',0,null,null),
('test8','cGFzc3dvcmQ=',0,null,null),
('test9','cGFzc3dvcmQ=',0,null,null),
('test10','cGFzc3dvcmQ=',0,null,null),
('test11','cGFzc3dvcmQ=',0,null,null),
('test12','cGFzc3dvcmQ=',0,null,null),
('test13','cGFzc3dvcmQ=',0,null,null),
('test14','cGFzc3dvcmQ=',0,null,null),
('test15','cGFzc3dvcmQ=',0,null,null),
('test16','cGFzc3dvcmQ=',0,null,null),
('test17','cGFzc3dvcmQ=',0,null,null),
('test18','cGFzc3dvcmQ=',0,null,null),
('test19','cGFzc3dvcmQ=',0,null,null),
('test20','cGFzc3dvcmQ=',0,null,null)


select * from dbo.[user]
where email='will@gmail.com'

insert into dbo.[REF_HOBI]
VALUES('Menggambar'),
('Dunia Bisnis'),
('Dunia Komputer'),
('Sains'),
('Politik'),
('Teknologi'),
('Bersosialisasi')
insert into dbo.REF_hasil_fakultas
VALUES('Ekonomi'),
('Hukum'),
('Teknik'),
('Kedokteran'),
('Psikologi'),
('Teknologi Informasi'),
('Seni Rupa dan Desain'),
('Ilmu Komunikasi')

select * from dbo.REF_HOBI
select * from dbo.REF_HASIL_FAKULTAS

-- Table for Admin--
select (m.first_name +' '+m.last_name) as Nama,
		rh.Hobi as Hobi,
		IIF(k.Buta_Warna=1,'Ya','Tidak') AS [Buta Warna],
		k.Matematika,
		k.Pkn,
		k.Tik,
		k.Fisika,
		k.Biologi,
		k.Kimia,
		isnull(rhf.nama_fakultas,'-') as [Fakultas]
        from dbo.mahasiswa m
left join dbo.kriteria k on m.kriteria_id=k.kriteria_id
left join dbo.REF_HOBI rh on rh.Hobi_id=k.hobi_id
left join dbo.REF_HASIL_FAKULTAS rhf on rhf.hasil_fakultas_id=m.hasil_fakultas_id
--Table for Data Testing --

SELECT	dt.Nama,
		rh.Hobi,
		IIF(dt.Buta_Warna=1,'Ya','Tidak') AS [Buta Warna],
		dt.Matematika,
		dt.Pkn,
		dt.Tik,
		dt.Fisika,
		dt.Biologi,
		dt.Kimia,
		rhf.Nama_Fakultas as [Fakultas]
FROM data_testing dt
join ref_hobi rh on rh.hobi_id=dt.hobi_id
join ref_hasil_fakultas rhf on rhf.hasil_fakultas_id=dt.hasil_fakultas_id
