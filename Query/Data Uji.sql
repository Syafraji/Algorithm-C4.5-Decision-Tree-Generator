use Project

select * from Data_Testing
Create table Data_Uji(
Data_Uji_Id bigint primary key identity,
Nama Varchar(50),
Buta_Warna bit,
Hobi_id bigint foreign key (Hobi_id) references [REF_HOBI](Hobi_id),
Matematika int,
Pkn int,
Tik int,
Fisika Int,
Biologi Int,
Kimia Int,
hasil_fakultas_id bigint foreign key (hasil_fakultas_id) references [REF_HASIL_FAKULTAS](hasil_fakultas_id))

select * from Data_Uji
select * from REF_HOBI
insert into dbo.Data_Uji
values
('Alena Anggraini'	,0,4,82,82,80,80,80,80,null),
('David Andrean'	,0,3,78,86,81,80,93,79,null),
('Albert Yang'		,0,3,85,91,83,90,87,81,null),
('Steven '			,0,3,84,93,94,95,88,86,null),
('Trisha Kaylie'	,0,1,94,98,81,100,88,84,null),
('Amy Anggriani'	,0,1,80,100,74,88,85,78,null),
('Jenifer'			,0,1,90,100,74,90,88,78,null),
('Nelson'			,0,2,80,81,80,85,88,77,null),
('Vimalaputri'		,0,1,88,75,74,75,88,77,null),
('Jacinda'			,0,7,88,95,80,85,88,80,null),
('Jeselyn Tania'	,0,3,88,86,80,83,86,79,null),
('Sherlina'			,0,1,88,86,80,85,88,88,null),
('Jocelyn Anggelina',0,1,85,96,80,85,98,80,null),
('Albert'			,0,4,75,75,74,75,78,77,null),
('Vincent Anderson ',0,2,82,75,80,80,83,79,null),
('Jeceline'			,0,2,86,92,80,92,86,83,null),
('Joni'				,0,2,77,75,76,85,77,77,null),
('Jeffry Anderson'	,0,4,86,78,86,88,89,78,null),
('El Primo'			,0,7,77,91,78,87,75,88,null),
('Willy Barney'		,0,3,95,93,90,78,89,76,null)
SELECT	dt.Data_Uji_Id,
                                        dt.Nama,
		                                rh.Hobi,
		                                IIF(dt.Buta_Warna=1,'Ya','Tidak') AS [Buta Warna],
		                                dt.Matematika,
		                                dt.Pkn,
		                                dt.Tik,
		                                dt.Fisika,
		                                dt.Biologi,
		                                dt.Kimia,
		                                rhf.Nama_Fakultas as [Fakultas]
		                                FROM data_uji dt
		                                join ref_hobi rh on rh.hobi_id=dt.hobi_id
		                                left join ref_hasil_fakultas rhf on rhf.hasil_fakultas_id=dt.hasil_fakultas_id