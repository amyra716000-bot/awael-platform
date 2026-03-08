                                                Table "public.exam_templates"
          Column           |            Type             | Collation | Nullable |                  Default                   
---------------------------+-----------------------------+-----------+----------+--------------------------------------------
 id                        | integer                     |           | not null | nextval('exam_templates_id_seq'::regclass)
 name                      | character varying           |           | not null | 
 type                      | examtype                    |           | not null | 
 stage_id                  | integer                     |           | not null | 
 subject_id                | integer                     |           |          | 
 section_id                | integer                     |           |          | 
 total_questions           | integer                     |           | not null | 
 duration_minutes          | integer                     |           | not null | 
 passing_score             | integer                     |           |          | 
 is_active                 | boolean                     |           |          | 
 start_date                | timestamp without time zone |           |          | 
 end_date                  | timestamp without time zone |           |          | 
 attempt_limit             | integer                     |           |          | 
 is_paid                   | boolean                     |           |          | 
 randomize_questions       | boolean                     |           |          | 
 randomize_options         | boolean                     |           |          | 
 leaderboard_enabled       | boolean                     |           |          | 
 show_answers_after_finish | boolean                     |           |          | 
 difficulty                | integer                     |           |          | 
 order                     | integer                     |           |          | 
Indexes:
    "exam_templates_pkey" PRIMARY KEY, btree (id)
    "ix_exam_templates_id" btree (id)
Foreign-key constraints:
    "exam_templates_section_id_fkey" FOREIGN KEY (section_id) REFERENCES sections(id)
    "exam_templates_stage_id_fkey" FOREIGN KEY (stage_id) REFERENCES stages(id)
    "exam_templates_subject_id_fkey" FOREIGN KEY (subject_id) REFERENCES subjects(id)
Referenced by:
    TABLE "exam_attempts" CONSTRAINT "exam_attempts_template_id_fkey" FOREIGN KEY (template_id) REFERENCES exam_templates(id)

