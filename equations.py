from sympy import *


# Current compensation value
def calculate_current_compensation_value(worker, param):
    LS, SEN, SGR, RET, DISR, t, p, q, ART14 = symbols('LastSalary Seniority Salary_Growth_Rate retirement_age Discount_Rate t p q Article14')
    part1 = LS * SEN * ART14 * ((((1 + SGR) ** (t + 0.5)) * p**t * q) / ((1 + DISR) ** (t + 0.5)))
    # print(part1)

    POS, RES = symbols('Property Resignation')
    part2 = POS * p * RES
    # print(part2)

    d = symbols('death')
    part3 = LS * SEN * (((1 + SGR) ** (t + 0.5) * p ** t * d) / ((1 + DISR) ** (t + 0.5)))
    # print(part3)

    # region Load values
    LS_VAL = worker.wage  # LastSalary
    SEN_VAL = worker.seniority  # Seniority
    RET_VAL = worker.retirementAge  # retirement_age
    SGR_VAL = param.pay_rise_rate  # Salary_Growth_Rate
    p_VAL = 1 - (param.dismissal + param.resignation + param.prob_death)  # p -  stay on the job probability
    q_VAL = param.dismissal  # q - fired from the job probability
    POS_VAL = worker.property  # Property
    d_VAL = param.prob_death  # death probability
    RES_VAL = param.resignation  # Resignation probability
    ART14_VAL = worker.article14  # article 14 percentage

    sub_dict = {
        LS: LS_VAL,
        SEN: SEN_VAL,
        RET: RET_VAL,
        SGR: SGR_VAL,
        p: p_VAL,
        q: q_VAL,
        POS: POS_VAL,
        d: d_VAL,
        RES: RES_VAL,
        ART14: ART14_VAL
    }
    # endregion

    formula = part1 + part2 + part3
    print(formula)
    est = 0
    for c_t in range(worker.retirementAge):
        sub_dict[t] = c_t  # Update t value
        sub_dict[DISR] = param.discount_rates[c_t + 1]  # Update discount rate value by params values
        res = float(formula.subs(sub_dict))  # Calculate value
        print(res)
        est += res  # sum all values
    return est
