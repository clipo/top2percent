tbn_df_ani_rw="temp_df_ani_rw"
savepath_ani_rw=basePath_project+"cache/"+ani_stamp+"/"+tbn_df_ani_rw
if file_exists(savepath_ani_rw):
  print("path already exists: "+savepath_ani_rw)
else:
  print ("Generating "+savepath_ani_rw)

  # reasons that would override the "error by journal" reason to still count it as an author-retraction.
  author_attributable_reasons=['Concerns/Issues with Peer Review','Rogue Editor','Unreliable Results','Concerns/Issues about Referencing/Attributions','Concerns/Issues About Data','Concerns/Issues About Results','Plagiarism of Article','Error in Data','Concerns/Issues About Image','Miscommunication by Author','Concerns/Issues About Authorship','Euphemisms for Plagiarism','Fake Peer Review','Error in Analyses','Error in Results and/or Conclusions','Unreliable Data','Not Presented at Conference','Lack of IRB/IACUC Approval','Randomly Generated Content','Hoax Paper','Taken from Dissertation/Thesis','Original Data not Provided','Bias Issues or Lack of Balance','Duplication of Image','Ethical Violations by Author','Conflict of Interest','Plagiarism of Text','Error in Materials (General)','Cites Retracted Work','Breach of Policy by Author']
  # 
  savepath_ani_rw_doi=savepath_ani_rw+'.doi'
  dbutils.fs.rm(savepath_ani_rw_doi,True)
  print ("Generating "+savepath_ani_rw_doi)

  df_rwdb_filtered_matching_columns=(
    spark.read.format('csv').option('header',True).load(os.path.join(basePath_project,'../',rw_dump))
    .filter('RetractionNature="Retraction"')
    .withColumn("ReasonList", func.filter(func.split(func.regexp_replace(func.col("Reason"), r"\+", ""), ';'), lambda x: x != ''))
    .withColumn(
      'JournalError_not_AuthorError',
      func.when(
        (func.arrays_overlap(func.col('ReasonList'),func.array(func.lit('Error by Journal/Publisher'),func.lit('Duplicate Publication through Error by Journal/Publisher'))))
        &(~func.arrays_overlap(func.col('ReasonList'),func.array(*[func.lit(x) for x in author_attributable_reasons])))
        ,func.lit(True)                                  
      ).otherwise(func.lit(False))
    )
    .withColumn(
      'Withdrawn_out_of_date_not_AuthorError',
      func.when(
        (func.array_contains(func.col('ReasonList'),'Withdrawn (out of date)'))
        &(~func.arrays_overlap(func.col('ReasonList'),func.array(*[func.lit(x) for x in author_attributable_reasons])))
        ,func.lit(True)                                  
      ).otherwise(func.lit(False))
    )
    .filter(func.col('JournalError_not_AuthorError')==False)
    .filter(func.col('Withdrawn_out_of_date_not_AuthorError')==False)
    .filter(~func.array_contains('ReasonList','Retract and Replace'))
    .withColumn('doi_normalized',normalize_doi(func.col('OriginalPaperDOI')))
    .withColumn('title_matcher',func.regexp_replace(func.lower("title"), '[^a-z0-9]', '').alias("title_matcher"))
    .withColumn("year_matcher_rw", func.regexp_extract("OriginalPaperDate", r"(\d{1,2})/(\d{1,2})/(\d{4})", 3).cast('long'))    
  )

  (
    df_ani
    .withColumn('doi_normalized',normalize_doi(func.col('doi')))
    .join(df_rwdb_filtered_matching_columns,'doi_normalized')        
    .select('eid','Record ID',func.lit('doi').alias('matchtype'))
    .distinct()
    .write.format("parquet").save(savepath_ani_rw_doi)
  )
  df_rw_doi=spark.read.format('parquet').load(savepath_ani_rw_doi)
  # get non-doi matches to match on title/year.
  savepath_ani_rw_titleyear=savepath_ani_rw+'.titleyear'
  dbutils.fs.rm(savepath_ani_rw_titleyear,True)
  print ("Generating "+savepath_ani_rw_titleyear)
  (
    df_ani
    .withColumn('title',func.coalesce(
      func.filter(
        func.col('citation_title'), 
        lambda x : (x.lang == 'eng')
      ).title[0],
      func.filter(
        func.col('citation_title'), 
        lambda x : (x.original == 'y')
      ).title[0],
    ))
    .withColumn('title_matcher',func.regexp_replace(func.lower("title"), '[^a-z0-9]', '').alias("title_matcher"))
    .filter(func.length('title_matcher')>=32) # minimum 32 characters title.
    .withColumn("year_matcher", func.col("sort_year"))
    .join(
      df_rwdb_filtered_matching_columns
      .join(df_rw_doi.select('Record ID').distinct(),'Record ID','LEFT_ANTI') # not previously matched on DOI.
      ,
      'title_matcher'
    )
    .filter(func.abs(func.col('year_matcher')-func.col('year_matcher_rw'))<=1) # years may differ one.
    .select('eid','Record ID',func.lit('titleyear').alias('matchtype'))
    .distinct()
    .write.format("parquet").save(savepath_ani_rw_titleyear)
  )
  # combine
  (
    spark.read.format('parquet').load(savepath_ani_rw_doi)
    .union(
      spark.read.format('parquet').load(savepath_ani_rw_titleyear)
    )
  ).write.format("parquet").save(savepath_ani_rw)
  # remove tmp:
  dbutils.fs.rm(savepath_ani_rw_doi,True)
  dbutils.fs.rm(savepath_ani_rw_titleyear,True)
df_ani_rw=spark.read.format('parquet').load(savepath_ani_rw).select('eid').distinct().withColumn('isRetracted',func.lit(True))