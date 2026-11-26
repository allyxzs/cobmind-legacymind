      ******************************************************************
      * CUSTMSTR.cbl - Cadastro e manutencao de clientes             *
      * Sistema: LEGACY-CRM (mainframe, COBOL-85)                     *
      * Reproduz um programa tipico de tela sequencial com arquivo    *
      * VSAM e calculo de limite de credito.                          *
      ******************************************************************
       IDENTIFICATION DIVISION.
       PROGRAM-ID. CUSTMSTR.
       AUTHOR. LEGACY TEAM.
       DATE-WRITTEN. 1987-03-12.

       ENVIRONMENT DIVISION.
       INPUT-OUTPUT SECTION.
       FILE-CONTROL.
           SELECT CUST-FILE ASSIGN TO VSAM-CUST
               ORGANIZATION IS INDEXED
               ACCESS MODE IS RANDOM
               RECORD KEY IS CUST-ID
               STATUS IS WS-STATUS.

       DATA DIVISION.
       FILE SECTION.
       FD  CUST-FILE.
       01  CUST-RECORD.
           05  CUST-ID            PIC X(8).
           05  CUST-NAME          PIC X(40).
           05  CUST-CLASS         PIC X.
           05  CUST-BALANCE       PIC 9(7)V99.
           05  CUST-LIMIT         PIC 9(7)V99.
           05  CUST-STATUS        PIC X.

       WORKING-STORAGE SECTION.
       01  WS-STATUS             PIC XX.
       01  WS-EOF                PIC X VALUE 'N'.
       01  WS-RATE               PIC 9(3)V99 VALUE 1.15.
       01  WS-TAX                PIC 9(3)V99 VALUE 0.0925.
       01  WS-FACTOR             PIC 9(3)V99.
       01  WS-TEMP-LIMIT         PIC 9(7)V99.

       PROCEDURE DIVISION.
       MAIN-PARA.
           PERFORM INIT-PARA
           PERFORM PROCESS-PARA UNTIL WS-EOF = 'Y'
           PERFORM CLOSE-PARA
           STOP RUN.

       INIT-PARA.
           OPEN INPUT CUST-FILE
           MOVE 'N' TO WS-EOF.

       PROCESS-PARA.
           READ CUST-FILE INTO CUST-RECORD
               AT END MOVE 'Y' TO WS-EOF
               NOT AT END PERFORM CALC-LIMIT-PARA
                           PERFORM WRITE-BACK-PARA.

       CALC-LIMIT-PARA.
           IF CUST-CLASS = 'A'
               MOVE 2.00 TO WS-FACTOR
           ELSE
               IF CUST-CLASS = 'B'
                   MOVE 1.50 TO WS-FACTOR
               ELSE
                   MOVE 1.00 TO WS-FACTOR
               END-IF
           END-IF.
           COMPUTE WS-TEMP-LIMIT = CUST-BALANCE * WS-RATE
           COMPUTE CUST-LIMIT = WS-TEMP-LIMIT * WS-FACTOR.
           COMPUTE CUST-LIMIT = CUST-LIMIT + (CUST-LIMIT * WS-TAX).

       WRITE-BACK-PARA.
           REWRITE CUST-RECORD
           DISPLAY 'CLIENTE ' CUST-ID ' LIMITE ' CUST-LIMIT.

       CLOSE-PARA.
           CLOSE CUST-FILE.