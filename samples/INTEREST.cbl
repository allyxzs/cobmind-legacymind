      ******************************************************************
      * INTEREST.cbl - Calculo de juros compostos e amortizacao       *
      * Regra de negocio financeira central do sistema de emprestimos.*
      ******************************************************************
       IDENTIFICATION DIVISION.
       PROGRAM-ID. INTEREST.
       DATA DIVISION.
       WORKING-STORAGE SECTION.
       01  WS-PRINCIPAL     PIC 9(9)V99 VALUE 10000.00.
       01  WS-ANNUAL-RATE   PIC 9(3)V99 VALUE 0.0725.
       01  WS-PERIODS       PIC 9(3)     VALUE 12.
       01  WS-YEARS         PIC 9(3)     VALUE 5.
       01  WS-TOTAL-PAYMENT PIC 9(11)V99.
       01  WS-MONTHLY-RATE  PIC 9(5)V9(6).
       01  WS-NPER          PIC 9(5).
       01  WS-EWMA          PIC 9(11)V99.
       PROCEDURE DIVISION.
       MAIN.
           COMPUTE WS-MONTHLY-RATE = WS-ANNUAL-RATE / 12
           COMPUTE WS-NPER = WS-PERIODS * WS-YEARS
           COMPUTE WS-TOTAL-PAYMENT = WS-PRINCIPAL *
               (1 + WS-MONTHLY-RATE) ** WS-NPER
           DISPLAY 'TOTAL A PAGAR: ' WS-TOTAL-PAYMENT
           STOP RUN.