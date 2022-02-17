
CREATE TABLE TFNTEST_AUDIT_CHANGES (
   AUDIT_DATE DATE,
   SESSION_USER VARCHAR2(100),
   OS_USER VARCHAR2(100),
   HOST VARCHAR2(100),
   OBJECT VARCHAR2(100),
   OBJECT_ID NUMBER,
   ACTION_TYPE VARCHAR2(500),
   ATTRIBUTE VARCHAR2(100),
   OLD_VALUE CLOB,
   NEW_VALUE CLOB
);


CREATE OR REPLACE TRIGGER CRM_CUSTOMERS_AUDIT_TRG
AFTER INSERT OR UPDATE OR DELETE ON CRM_CUSTOMERS
   REFERENCING OLD AS OLD NEW AS NEW
   FOR EACH ROW
DECLARE
   V_TABLE        ALL_TAB_COLUMNS.TABLE_NAME%TYPE := 'CRM_CUSTOMERS';
   V_OBJECT       TFNTEST_AUDIT_CHANGES.OBJECT_ID%TYPE;
   V_ATTRIBUTE    TFNTEST_AUDIT_CHANGES.ATTRIBUTE%TYPE;
   V_OLD_VALUE    TFNTEST_AUDIT_CHANGES.OLD_VALUE%TYPE;
   V_NEW_VALUE    TFNTEST_AUDIT_CHANGES.NEW_VALUE%TYPE;
   function GET_OLD_VALUE(COLUMN_NAME ALL_TAB_COLUMNS.COLUMN_NAME%TYPE) RETURN CLOB IS
      V_RET CLOB;
   BEGIN
      IF COLUMN_NAME = 'ID' THEN V_RET := TO_CLOB(:OLD.ID);
      ELSIF COLUMN_NAME = 'NAMES' THEN V_RET := TO_CLOB(:OLD.NAMES);
      ELSIF COLUMN_NAME = 'LAST_NAMES' THEN V_RET := TO_CLOB(:OLD.LAST_NAMES);
      ELSIF COLUMN_NAME = 'BIRTH_DATE' THEN V_RET := TO_CLOB(:OLD.BIRTH_DATE);
      ELSIF COLUMN_NAME = 'NOTES' THEN V_RET := TO_CLOB(:OLD.NOTES);
      END IF;
      RETURN V_RET;
   END;
   function GET_NEW_VALUE(COLUMN_NAME ALL_TAB_COLUMNS.COLUMN_NAME%TYPE) RETURN CLOB IS
      V_RET CLOB;
   BEGIN
      IF COLUMN_NAME = 'ID' THEN V_RET := TO_CLOB(:NEW.ID);
      ELSIF COLUMN_NAME = 'NAMES' THEN V_RET := TO_CLOB(:NEW.NAMES);
      ELSIF COLUMN_NAME = 'LAST_NAMES' THEN V_RET := TO_CLOB(:NEW.LAST_NAMES);
      ELSIF COLUMN_NAME = 'BIRTH_DATE' THEN V_RET := TO_CLOB(:NEW.BIRTH_DATE);
      ELSIF COLUMN_NAME = 'NOTES' THEN V_RET := TO_CLOB(:NEW.NOTES);
      END IF;
      RETURN V_RET;
   END;
BEGIN
/*--------------------------------------------------------------*/
   IF INSERTING THEN
      V_OBJECT := :NEW.ID;
   ELSE
      V_OBJECT := :OLD.ID;
   END IF;

   FOR I IN (SELECT * FROM ALL_TAB_COLUMNS WHERE TABLE_NAME = V_TABLE ORDER BY COLUMN_ID) LOOP
      IF INSERTING THEN
         V_NEW_VALUE := GET_NEW_VALUE(I.COLUMN_NAME);
         INSERT INTO TFNTEST_AUDIT_CHANGES
         VALUES (
            SYSDATE,
            SYS_CONTEXT('USERENV','SESSION_USER'),
            SYS_CONTEXT('USERENV','OS_USER'),
            SYS_CONTEXT('USERENV','HOST'),
            V_TABLE,
            V_OBJECT,
            'I',
            I.COLUMN_NAME,
            NULL,
            V_NEW_VALUE
         );
      ELSIF UPDATING THEN
         V_OLD_VALUE := GET_OLD_VALUE(I.COLUMN_NAME);
         V_NEW_VALUE := GET_NEW_VALUE(I.COLUMN_NAME);
         IF V_NEW_VALUE != V_OLD_VALUE THEN
            INSERT INTO TFNTEST_AUDIT_CHANGES
            VALUES (
               SYSDATE,
               SYS_CONTEXT('USERENV','SESSION_USER'),
               SYS_CONTEXT('USERENV','OS_USER'),
               SYS_CONTEXT('USERENV','HOST'),
               V_TABLE,
               V_OBJECT,
               'U',
               I.COLUMN_NAME,
               V_OLD_VALUE,
               V_NEW_VALUE
            );
         END IF;
      ELSIF DELETING THEN
         V_OLD_VALUE := GET_OLD_VALUE(I.COLUMN_NAME);
         INSERT INTO TFNTEST_AUDIT_CHANGES
         VALUES (
            SYSDATE,
            SYS_CONTEXT('USERENV','SESSION_USER'),
            SYS_CONTEXT('USERENV','OS_USER'),
            SYS_CONTEXT('USERENV','HOST'),
            V_TABLE,
            V_OBJECT,
            'D',
            I.COLUMN_NAME,
            V_OLD_VALUE,
            NULL
         );
      END IF;
   END LOOP;
/*--------------------------------------------------------------*/
END;
/

CREATE OR REPLACE TRIGGER CRM_CUSTOMER_ADDRESSES_AUDIT_TRG
AFTER INSERT OR UPDATE OR DELETE ON CRM_CUSTOMER_ADDRESSES
   REFERENCING OLD AS OLD NEW AS NEW
   FOR EACH ROW
DECLARE
   V_TABLE        ALL_TAB_COLUMNS.TABLE_NAME%TYPE := 'CRM_CUSTOMER_ADDRESSES';
   V_OBJECT       TFNTEST_AUDIT_CHANGES.OBJECT_ID%TYPE;
   V_ATTRIBUTE    TFNTEST_AUDIT_CHANGES.ATTRIBUTE%TYPE;
   V_OLD_VALUE    TFNTEST_AUDIT_CHANGES.OLD_VALUE%TYPE;
   V_NEW_VALUE    TFNTEST_AUDIT_CHANGES.NEW_VALUE%TYPE;
   function GET_OLD_VALUE(COLUMN_NAME ALL_TAB_COLUMNS.COLUMN_NAME%TYPE) RETURN CLOB IS
      V_RET CLOB;
   BEGIN
      IF COLUMN_NAME = 'ID' THEN V_RET := TO_CLOB(:OLD.ID);
      ELSIF COLUMN_NAME = 'CUSTOMER_ID' THEN V_RET := TO_CLOB(:OLD.CUSTOMER_ID);
      ELSIF COLUMN_NAME = 'ADDRESS_TYPE' THEN V_RET := TO_CLOB(:OLD.ADDRESS_TYPE);
      ELSIF COLUMN_NAME = 'ADDRESS' THEN V_RET := TO_CLOB(:OLD.ADDRESS);
      END IF;
      RETURN V_RET;
   END;
   function GET_NEW_VALUE(COLUMN_NAME ALL_TAB_COLUMNS.COLUMN_NAME%TYPE) RETURN CLOB IS
      V_RET CLOB;
   BEGIN
      IF COLUMN_NAME = 'ID' THEN V_RET := TO_CLOB(:NEW.ID);
      ELSIF COLUMN_NAME = 'CUSTOMER_ID' THEN V_RET := TO_CLOB(:NEW.CUSTOMER_ID);
      ELSIF COLUMN_NAME = 'ADDRESS_TYPE' THEN V_RET := TO_CLOB(:NEW.ADDRESS_TYPE);
      ELSIF COLUMN_NAME = 'ADDRESS' THEN V_RET := TO_CLOB(:NEW.ADDRESS);
      END IF;
      RETURN V_RET;
   END;
BEGIN
/*--------------------------------------------------------------*/
   IF INSERTING THEN
      V_OBJECT := :NEW.ID;
   ELSE
      V_OBJECT := :OLD.ID;
   END IF;

   FOR I IN (SELECT * FROM ALL_TAB_COLUMNS WHERE TABLE_NAME = V_TABLE ORDER BY COLUMN_ID) LOOP
      IF INSERTING THEN
         V_NEW_VALUE := GET_NEW_VALUE(I.COLUMN_NAME);
         INSERT INTO TFNTEST_AUDIT_CHANGES
         VALUES (
            SYSDATE,
            SYS_CONTEXT('USERENV','SESSION_USER'),
            SYS_CONTEXT('USERENV','OS_USER'),
            SYS_CONTEXT('USERENV','HOST'),
            V_TABLE,
            V_OBJECT,
            'I',
            I.COLUMN_NAME,
            NULL,
            V_NEW_VALUE
         );
      ELSIF UPDATING THEN
         V_OLD_VALUE := GET_OLD_VALUE(I.COLUMN_NAME);
         V_NEW_VALUE := GET_NEW_VALUE(I.COLUMN_NAME);
         IF V_NEW_VALUE != V_OLD_VALUE THEN
            INSERT INTO TFNTEST_AUDIT_CHANGES
            VALUES (
               SYSDATE,
               SYS_CONTEXT('USERENV','SESSION_USER'),
               SYS_CONTEXT('USERENV','OS_USER'),
               SYS_CONTEXT('USERENV','HOST'),
               V_TABLE,
               V_OBJECT,
               'U',
               I.COLUMN_NAME,
               V_OLD_VALUE,
               V_NEW_VALUE
            );
         END IF;
      ELSIF DELETING THEN
         V_OLD_VALUE := GET_OLD_VALUE(I.COLUMN_NAME);
         INSERT INTO TFNTEST_AUDIT_CHANGES
         VALUES (
            SYSDATE,
            SYS_CONTEXT('USERENV','SESSION_USER'),
            SYS_CONTEXT('USERENV','OS_USER'),
            SYS_CONTEXT('USERENV','HOST'),
            V_TABLE,
            V_OBJECT,
            'D',
            I.COLUMN_NAME,
            V_OLD_VALUE,
            NULL
         );
      END IF;
   END LOOP;
/*--------------------------------------------------------------*/
END;
/


CREATE OR REPLACE TRIGGER CRM_CUSTOMER_DOCUMENTS_AUDIT_TRG
AFTER INSERT OR UPDATE OR DELETE ON CRM_CUSTOMER_DOCUMENTS
   REFERENCING OLD AS OLD NEW AS NEW
   FOR EACH ROW
DECLARE
   V_TABLE        ALL_TAB_COLUMNS.TABLE_NAME%TYPE := 'CRM_CUSTOMER_DOCUMENTS';
   V_OBJECT       TFNTEST_AUDIT_CHANGES.OBJECT_ID%TYPE;
   V_ATTRIBUTE    TFNTEST_AUDIT_CHANGES.ATTRIBUTE%TYPE;
   V_OLD_VALUE    TFNTEST_AUDIT_CHANGES.OLD_VALUE%TYPE;
   V_NEW_VALUE    TFNTEST_AUDIT_CHANGES.NEW_VALUE%TYPE;
   function GET_OLD_VALUE(COLUMN_NAME ALL_TAB_COLUMNS.COLUMN_NAME%TYPE) RETURN CLOB IS
      V_RET CLOB;
   BEGIN
      IF COLUMN_NAME = 'ID' THEN V_RET := TO_CLOB(:OLD.ID);
      ELSIF COLUMN_NAME = 'CUSTOMER_ID' THEN V_RET := TO_CLOB(:OLD.CUSTOMER_ID);
      ELSIF COLUMN_NAME = 'DOCUMENT_TYPE' THEN V_RET := TO_CLOB(:OLD.DOCUMENT_TYPE);
      ELSIF COLUMN_NAME = 'DOCUMENT' THEN V_RET := TO_CLOB(:OLD.DOCUMENT);
      END IF;
      RETURN V_RET;
   END;
   function GET_NEW_VALUE(COLUMN_NAME ALL_TAB_COLUMNS.COLUMN_NAME%TYPE) RETURN CLOB IS
      V_RET CLOB;
   BEGIN
      IF COLUMN_NAME = 'ID' THEN V_RET := TO_CLOB(:NEW.ID);
      ELSIF COLUMN_NAME = 'CUSTOMER_ID' THEN V_RET := TO_CLOB(:NEW.CUSTOMER_ID);
      ELSIF COLUMN_NAME = 'DOCUMENT_TYPE' THEN V_RET := TO_CLOB(:NEW.DOCUMENT_TYPE);
      ELSIF COLUMN_NAME = 'DOCUMENT' THEN V_RET := TO_CLOB(:NEW.DOCUMENT);
      END IF;
      RETURN V_RET;
   END;
BEGIN
/*--------------------------------------------------------------*/
   IF INSERTING THEN
      V_OBJECT := :NEW.ID;
   ELSE
      V_OBJECT := :OLD.ID;
   END IF;

   FOR I IN (SELECT * FROM ALL_TAB_COLUMNS WHERE TABLE_NAME = V_TABLE ORDER BY COLUMN_ID) LOOP
      IF INSERTING THEN
         V_NEW_VALUE := GET_NEW_VALUE(I.COLUMN_NAME);
         INSERT INTO TFNTEST_AUDIT_CHANGES
         VALUES (
            SYSDATE,
            SYS_CONTEXT('USERENV','SESSION_USER'),
            SYS_CONTEXT('USERENV','OS_USER'),
            SYS_CONTEXT('USERENV','HOST'),
            V_TABLE,
            V_OBJECT,
            'I',
            I.COLUMN_NAME,
            NULL,
            V_NEW_VALUE
         );
      ELSIF UPDATING THEN
         V_OLD_VALUE := GET_OLD_VALUE(I.COLUMN_NAME);
         V_NEW_VALUE := GET_NEW_VALUE(I.COLUMN_NAME);
         IF V_NEW_VALUE != V_OLD_VALUE THEN
            INSERT INTO TFNTEST_AUDIT_CHANGES
            VALUES (
               SYSDATE,
               SYS_CONTEXT('USERENV','SESSION_USER'),
               SYS_CONTEXT('USERENV','OS_USER'),
               SYS_CONTEXT('USERENV','HOST'),
               V_TABLE,
               V_OBJECT,
               'U',
               I.COLUMN_NAME,
               V_OLD_VALUE,
               V_NEW_VALUE
            );
         END IF;
      ELSIF DELETING THEN
         V_OLD_VALUE := GET_OLD_VALUE(I.COLUMN_NAME);
         INSERT INTO TFNTEST_AUDIT_CHANGES
         VALUES (
            SYSDATE,
            SYS_CONTEXT('USERENV','SESSION_USER'),
            SYS_CONTEXT('USERENV','OS_USER'),
            SYS_CONTEXT('USERENV','HOST'),
            V_TABLE,
            V_OBJECT,
            'D',
            I.COLUMN_NAME,
            V_OLD_VALUE,
            NULL
         );
      END IF;
   END LOOP;
/*--------------------------------------------------------------*/
END;
/
