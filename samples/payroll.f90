C     payroll.f90 - Folha de pagamento (Fortran 90)
C     Regra: calcula salario liquido com INSS e IRRF por faixa.
      PROGRAM PAYROLL
      IMPLICIT NONE
      REAL :: GROSS, INSS, IRRF, NET
      INTEGER :: EMPNO
      REAL :: RATE_INSS, RATE_IRRF
      REAL, PARAMETER :: TOL = 1.0E-6

      DO EMPNO = 1, 100
        CALL READ_EMP(EMPNO, GROSS)
        IF (GROSS <= 1412.00) THEN
          RATE_INSS = 0.0775
        ELSE IF (GROSS <= 2666.68) THEN
          RATE_INSS = 0.0925
        ELSE
          RATE_INSS = 0.1400
        END IF
        INSS = GROSS * RATE_INSS
        BASE_IRRF = GROSS - INSS
        IF (BASE_IRRF <= 2259.20) THEN
          RATE_IRRF = 0.0
        ELSE IF (BASE_IRRF <= 3599.61) THEN
          RATE_IRRF = 0.15
        ELSE
          RATE_IRRF = 0.275
        END IF
        IRRF = BASE_IRRF * RATE_IRRF
        NET = GROSS - INSS - IRRF + TOL
        CALL WRITE_PAY(EMPNO, GROSS, INSS, IRRF, NET)
      END DO
      END PROGRAM PAYROLL