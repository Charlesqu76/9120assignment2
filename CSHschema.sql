DROP TABLE IF EXISTS Administrator;
DROP TABLE IF EXISTS Patient;
DROP TABLE IF EXISTS AdmissionType;
DROP TABLE IF EXISTS Department;
DROP TABLE IF EXISTS Admission;



-- del 
SET DateStyle = 'DMY';

CREATE TABLE Administrator (
    UserName VARCHAR(10) PRIMARY KEY,
    Password VARCHAR(20) NOT NULL,
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50) NOT NULL,
    Email VARCHAR(20) NOT NULL
);

INSERT INTO Administrator VALUES 
('jdoe', 'Pass1234', 'John', 'Doe', 'jdoe@csh.com'),
('jsmith', 'Pass5678', 'Jane', 'Smith', 'jsmith@csh.com'),
('ajohnson', 'Passabcd', 'Alice', 'Johnson', 'ajohnson@csh.com'),
('bbrown', 'Passwxyz', 'Bob', 'Brown', 'bbrown@csh.com'),
('cdavis', 'Pass9876', 'Charlie', 'Davis', 'cdavis@csh.com'),
('ksmith', 'Pass5566', 'Karen', 'Smith', 'ksmith@csh.com');

CREATE TABLE Patient (
    PatientID VARCHAR(10) PRIMARY KEY,
    Password VARCHAR(20) NOT NULL,
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50) NOT NULL,
    Mobile VARCHAR(20) NOT NULL
);

INSERT INTO Patient VALUES 
('dwilson', 'Pass5432', 'David', 'Wilson', '4455667788'),
('etylor', 'Passlmno', 'Eva', 'Taylor', '5566778899'),
('faderson', 'Passrstu', 'Frank', 'Anderson', '6677889900'),
('gthomas', 'Pass1357', 'Grace', 'Thomas', '7788990011'),
('smartinez', 'Pass2468', 'Stan', 'Martinez', '8899001122'),
('lroberts', 'Pass1122', 'Laura', 'Roberts', '9900112233');


CREATE TABLE AdmissionType (
    AdmissionTypeID SERIAL PRIMARY KEY,
    AdmissionTypeName VARCHAR(20) UNIQUE NOT NULL
);

INSERT INTO AdmissionType VALUES (1, 'Emergency');
INSERT INTO AdmissionType VALUES (2, 'Transfer');
INSERT INTO AdmissionType VALUES (3, 'Inpatient');
INSERT INTO AdmissionType VALUES (4, 'Outpatient');

CREATE TABLE Department (
    DeptId SERIAL PRIMARY Key,
    DeptName VARCHAR(20) UNIQUE not NULL
);

INSERT INTO Department VALUES (1, 'General');
INSERT INTO Department VALUES (2, 'Emergency');
INSERT INTO Department VALUES (3, 'Surgery');
INSERT INTO Department VALUES (4, 'Obstetrics');
INSERT INTO Department VALUES (5, 'Rehabilitation');
INSERT INTO Department VALUES (6, 'Paediatrics');

CREATE table Admission (
    AdmissionID SERIAL PRIMARY KEY,
    AdmissionType INTEGER NOT NULL,
    Department INTEGER NOT NULL,
	Patient VARCHAR(10) NOT NULL,
	Administrator VARCHAR(10) NOT NULL,
    Fee Decimal(7,2),
    DischargeDate Date,
    Condition VARCHAR(500),
	FOREIGN KEY(AdmissionType) REFERENCES AdmissionType,
	FOREIGN KEY(Department) REFERENCES Department,
	FOREIGN KEY(Patient) REFERENCES Patient,
	FOREIGN KEY(Administrator) REFERENCES Administrator
);

INSERT INTO Admission (AdmissionType, Department, Fee, Patient, Administrator, DischargeDate, Condition) VALUES
    (4, 1, 666.00, 'lroberts', 'jdoe', '28/02/2024', 'a red patch on my skin that looks irritated. It started small but has been spreading and feels warm to the touch'),
	(2, 1, 100.00, 'gthomas', 'jdoe', '11/09/2021', NULL),
	(1, 2, NULL, 'lroberts','jsmith', '02/09/2019', 'Admitted to the emergency department after suffering head trauma from a fall, requiring a CT scan and observation for potential concussion.'),
	(2, 3, 7688.00, 'dwilson','ajohnson', '01/12/2022', NULL),
	(2, 6, 1600.00, 'faderson', 'ajohnson', '03/09/2014', 'Child admitted to the hospital with a severe asthma attack, requiring oxygen therapy and nebulizer treatment.'),
	(4, 1, 90.00, 'gthomas', 'ksmith', '04/07/2021', 'Routine follow-up consultation to review progress after recent knee surgery, with positive recovery observed.'),
	(1, 2, 1450.00, 'smartinez', 'jsmith', NULL, 'Admitted to the emergency department with severe food poisoning, requiring IV fluids and anti-nausea medication for recovery.'),
	(4, 5, 180.95, 'dwilson', 'cdavis', '06/11/2021', 'Attended a physiotherapy session as part of an ongoing rehabilitation program following shoulder surgery.'),
	(3, 1, 2000.00, 'etylor', 'ajohnson', '10/09/2021', NULL),
	(2, 4, 8290.00, 'gthomas', 'jsmith', '01/09/2024', 'Postpartum care following a natural childbirth, including monitoring of both the mother and the newborn for potential complications.'),
	(2, 6, 1800.00, 'faderson', 'bbrown',  NULL, 'Child admitted to the paediatrics department for severe pneumonia, requiring intravenous antibiotics and respiratory therapy.'),
	(4, 1, 75.00, 'gthomas', 'bbrown', '19/11/2023', 'Routine general practitioner consultation for a follow-up after a recent bout of seasonal allergies.'),
	(3, 3, 7000.50, 'smartinez', 'jdoe', '15/10/2024', NULL),
	(1, 2, NULL, 'etylor', 'jdoe', NULL, 'I am having intense, crushing pain in my chest that feels like an elephant is sitting on it. It is spreading to my left arm and neck.');

-- Create the stored function to find the associated admission list of the adminstrator.
CREATE OR REPLACE FUNCTION findAdmissionsByadmin(Login_name VARCHAR)
RETURNS table(
    Admission_id INT,
    Admission_type VARCHAR(20),
    Admission_department VARCHAR(20),
    Discharge_date TEXT,
    Fee VARCHAR,
    Patient TEXT,
    Condition VARCHAR(500)
) AS $$
BEGIN 
    REtURN QUERY
    SELECT ad.AdmissionID as "ID", admit.AdmissionTypeName as "Type", 
           dept.DeptName as "Department", COALESCE(TO_CHAR(ad.DischargeDate, 'DD-MM-YYYY'), '') as "Discharge Date", 
           COALESCE(ad.Fee::varchar, '') as "Fee", concat(pt.FirstName, ' ', pt.LastName) as "Patient", 
           COALESCE(ad.Condition, '') as "Condition"
    FROM Admission ad 
         INNER JOIN AdmissionType admit ON(ad.AdmissionType = admit.AdmissionTypeID) 
         INNER JOIN Department dept ON(ad.department = dept.DeptId)
         INNER JOIN Patient pt ON(ad.Patient = pt.PatientID)
         INNER JOIN Administrator admini ON(ad.Administrator = admini.UserName)
    WHERE ad.Administrator = Login_name
    ORDER BY ad.DischargeDate DESC NULLS LAST, pt.FirstName ASC, 
             pt.LastName ASC, admit.AdmissionTypeName DESC; 
END;
$$ LANGUAGE plpgsql; 



CREATE OR REPLACE FUNCTION findadmissionsbycriteria("searchstring" varchar)
  RETURNS TABLE("admission_id" int4, "admission_type" varchar, "admission_department" varchar, "discharge_date" text, "fee" varchar, "patient" text, "condition" varchar) AS $BODY$
	DECLARE
   _searchstring varchar := ('%' ||LOWER(searchstring)|| '%');
	BEGIN
	RETURN QUERY
  SELECT A.admissionid AS admission_id,
	AT.AdmissionTypeName AS admission_type,
	D.DeptName AS admission_department,
	COALESCE(TO_CHAR(A.DischargeDate, 'DD-MM-YYYY'), '') AS discharge_date,
	COALESCE(A.Fee::varchar, '') AS fee,
	P.FirstName ||' ' || P.LastName AS patient,
	COALESCE(A.CONDITION, '') AS condition 
FROM
	Admission
	AS A LEFT JOIN AdmissionType AS AT ON A.AdmissionType = AT.AdmissionTypeID
	LEFT JOIN Department AS D ON A.Department = D.DeptId
	LEFT JOIN Patient AS P ON A.Patient = P.PatientID 
WHERE
	(
		LOWER ( A.CONDITION ) LIKE   _searchstring 
		OR LOWER ( AT.AdmissionTypeName ) LIKE   _searchstring 
		OR LOWER ( D.DeptName ) LIKE   _searchstring
		OR LOWER ( P.FirstName ) LIKE   _searchstring  
		OR LOWER ( P.LastName ) LIKE   _searchstring 
	) 
	AND ( A.DischargeDate IS NULL OR A.DischargeDate >= CURRENT_DATE - INTERVAL '2 years' ) 
ORDER BY
	A.DischargeDate IS NOT NULL,
	A.DischargeDate,
	P.FirstName,
	P.LastName;

END
$BODY$
  LANGUAGE plpgsql;




  CREATE OR REPLACE FUNCTION addAdmission("type_" varchar, "department_" varchar, "patient_" varchar, "condition_" varchar, "admin_" varchar)
  RETURNS BOOL AS $BODY$
	DECLARE
		type_id INT;
		department_id INT;
		patient_id VARCHAR;
		
	BEGIN
	
SELECT AdmissionTypeID INTO type_id FROM AdmissionType WHERE LOWER(type_) = LOWER(AdmissionTypeName);
	IF  type_id IS NULL 
	THEN RETURN FALSE;
	END IF;
	
	
 SELECT DeptId INTO department_id FROM Department WHERE LOWER(department_) = LOWER(DeptName);
	IF  department_id IS NULL
	THEN RETURN FALSE;
	END IF;
	
	SELECT PatientID INTO patient_id FROM Patient WHERE  LOWER(PatientID) = LOWER(patient_);
	IF  patient_id IS NULL
	THEN RETURN FALSE;
	END IF;
	
	INSERT INTO Admission(AdmissionType, Department,Patient ,Administrator, Condition) 
	VALUES (type_id, department_id, patient_id,admin_, condition_ );
	
	RETURN TRUE;
		
END
$BODY$
  LANGUAGE plpgsql;