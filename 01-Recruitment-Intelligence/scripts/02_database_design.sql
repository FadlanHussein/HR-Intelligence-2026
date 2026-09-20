CREATE TABLE recruitment_candidates (
    candidate_id SERIAL PRIMARY KEY,
    age INTEGER,
    gender VARCHAR(20),
    education_level VARCHAR(50),
    experience_years INTEGER,
    previous_companies INTEGER,
    distance_from_company NUMERIC,
    interview_score INTEGER,
    skill_score INTEGER,
    personality_score INTEGER,
    recruitment_strategy VARCHAR(20),
    hiring_decision INTEGER,
    CONSTRAINT chk_age CHECK (age BETWEEN 20 AND 50),
    CONSTRAINT chk_experience CHECK (experience_years BETWEEN 0 AND 15),
    CONSTRAINT chk_previous_companies CHECK (previous_companies BETWEEN 1 AND 5),
    CONSTRAINT chk_interview_score CHECK (interview_score BETWEEN 0 AND 100),
    CONSTRAINT chk_skill_score CHECK (skill_score BETWEEN 0 AND 100),
    CONSTRAINT chk_personality_score CHECK (personality_score BETWEEN 0 AND 100),
    CONSTRAINT chk_hiring_decision CHECK (hiring_decision IN (0, 1))
);

  

