from sympy import *
from print_colors import col


def print_res(message, res):
    """ Prints the result with color """
    print(f'{col.OKBLUE}{message}: {res}{col.ENDC}')

# region ========================= MAIN PART 1 =========================


# region <!--- PART 1 : Current compensation value  ---!>
def calculate_current_compensation_value(worker, param):
    """
    Calculating the current compensation value based on long equation.
    To build the final equation the function uses 3 part equation.
    After the calculation finished the results is set to worker object - worker.CCV
    """
    LS, SEN, SGR, RET, DISR, t, p, q, ART14_1 = symbols('LastSalary Seniority1 Salary_Growth_Rate retirement_age Discount_Rate t p q Article14_1')
    part1 = LS * SEN * ART14_1 * ((((1 + SGR) ** (t + 0.5)) * p**t * q) / ((1 + DISR) ** (t + 0.5)))
    # print(part1)

    POS, RES = symbols('Property Resignation')
    part2 = POS * p * RES
    # print(part2)

    d, SEN2, ART14_2 = symbols('death Seniority2 Article14_1')
    part3 = LS * SEN2 * ART14_2 * (((1 + SGR) ** (t + 0.5) * p ** t * d) / ((1 + DISR) ** (t + 0.5)))
    # print(part3)

    # region Load values
    LS_VAL = worker.wage  # LastSalary
    SEN_VAL = worker.seniority  # Seniority
    RET_VAL = worker.retirementAge  # retirement_age
    SGR_VAL = param.pay_rise  # Salary_Growth_Rate
    p_VAL = 1 - (param.departure_probabilities(worker.age)[0] + param.departure_probabilities(worker.age)[1] + param.male_deathTable[worker.age] if worker.gender == 0 else param.female_deathTable[worker.age])  # p -  stay on the job probability
    q_VAL = param.departure_probabilities(worker.age)[0]  # q - fired from the job probability
    POS_VAL = worker.property  # Property
    d_VAL = param.male_deathTable[worker.age] if worker.gender == 0 else param.female_deathTable[worker.age]  # death probability
    RES_VAL = param.departure_probabilities(worker.age)[1]  # Resignation probability
    ART14_VAL = worker.article14  # article 14 percentage

    sub_dict = dict()  # declaration
    if worker.complex_a_14 is False:
        sub_dict = {
            LS: LS_VAL,
            SEN: SEN_VAL,
            SEN2: SEN_VAL,
            RET: RET_VAL,
            SGR: SGR_VAL,
            p: p_VAL,
            q: q_VAL,
            POS: POS_VAL,
            d: d_VAL,
            RES: RES_VAL,
            ART14_1: ART14_VAL,
            ART14_2: ART14_VAL
        }
    # endregion

    formula = part1 + part2 + part3
    # print(formula)
    est = 0
    for c_t in range(worker.yearsToWork):
        sub_dict[t] = c_t  # Update t value
        sub_dict[DISR] = param.interest_rate[c_t + 1]  # Update discount rate value by params values
        res = float(formula.subs(sub_dict))  # Calculate value
        # print(res)
        est += res  # sum all values

    print_res('Calculated CCV - Current Compensation Value', est)
    worker.CCV = est
    return est
# endregion


# region <!--- PART 2 : Current service cost ---!>
def current_service_cost(worker, partOfYear):
    """
    Calculates the service cost.
    :param worker: Worker object with all the specific worker data [Worker obj]
    :param partOfYear: What part of the year the worker worked [float]
    After the calculation finished the results is set to worker object - worker.CSC
    """
    if worker.article14 == 1:
        print(f'{col.OKGREEN}For worker with ARTICLE 14  = 100% cannot compute Current Service Cost {col.ENDC}')
        return

    if worker.CCV == -1:
        raise ValueError('Current compensation value Needed - use calculate_current_compensation_value function')

    # Actuarial factor - AF
    CCV, LS, SEN, ART14 = symbols('Current_Compensation_Value Last_Salary Seniority Article14')
    AF_RES = (CCV) / (LS * SEN * (1 - ART14))

    # Current Service Cost - CSC
    POY, AF = symbols('Part_Of_Year Actuarial_Factor')
    CSC = LS * POY * (1 - ART14) * AF

    AF_dict = {
        LS: worker.wage,
        SEN: worker.seniority,
        ART14: worker.article14 + 1 if worker.article14 != 0 else 0,
        CCV: worker.CCV
    }

    # Calculation results of Actuarial factor
    CALC_AF = AF_RES.subs(AF_dict)

    CSC_dict = {
        LS: worker.wage,
        POY: partOfYear,
        ART14: worker.article14 + 1 if worker.article14 != 0 else 0,
        AF: CALC_AF
    }

    # Calculate the total cost
    COST = CSC.subs(CSC_dict)
    print_res('Calculated CSC - Current Service Cost', COST)
    worker.CSC = COST
    return COST
# endregion


# region <!--- PART 3 : Interest (Capitalization) ---!>
def calculate_interest_for_one_worker(worker, param):
    # TODO change worker to workers => supposed to be calculation on number of workers just add a loop afterwards
    """
    # TODO check how the E(t) needed in the equation calc
    Calculates the E(t) of the worker
    worker.calc_service_expectancy(param.prob_death, param.resignation, param.dismissal, currentAge=20)
    """
    def get_current_age(cur_worker, cur_year):
        return cur_year - cur_worker.birthday.year

    # Calculate E(t) function
    DIS, DEATH = symbols('dismissal_chance death_chance')
    et = (1 - DIS - DEATH)
    et_est = 0
    start_year = worker.start_work.year  # save the year started working
    for year in range(worker.yearsToWork):
        current_age = get_current_age(worker, start_year + year)
        dis_values = sum(param.departure_probabilities(current_age))
        death_table = param.male_deathTable[worker.age] if worker.gender == 0 else param.female_deathTable[worker.age]
        et_dict = {
            DIS: dis_values,
            DEATH: death_table
        }
        et_est += et.subs(et_dict)

    et_est = round(et_est)
    worker.eT = param.interest_rate[et_est]

    CCV, DR, CSC, BP = symbols('Current_Compensation_Value Discount_Rate Current_Service_Cost Benefits_Paid')
    eq = (CCV * DR) + ((CSC - BP) * (DR / 2))

    ci_dict = {
        CCV: worker.CCV,
        DR: worker.eT,
        CSC: worker.CSC,
        BP: worker.benefits_paid
    }

    # For one worker
    interest = eq.subs(ci_dict)
    worker.cost_of_capitalization = interest
    print_res('Current interest: ', interest)

    return interest
# endregion


# region <!--- PART4 : Benefits paid ---!>
def calculate_benefits_paid(workers_list):
    est = 0
    for worker in workers_list:
        est += worker.benefits_paid
    print_res('Benefits Paid: ', est)
    return est
# endregion


# region <!--- PART5 : Actuarial losses ---!>
def calculate_actuarial_losses(CCCB, CCV, CSC, INTEREST, BP):
    """
    :param CCCB: Current Compensation Closing Balance
    :param CCV: Current Compensation Values
    :param CSC: Current Service Cost
    :param INTEREST: Interest (Part3)
    :param BP: Benefits Paid
    :return: Actuarial Losses float value
    """
    return CCCB - CCV - CSC - INTEREST + BP
# endregion


# region <!--- PART6 : Present value Commitment to closing balance ---!>
def calculate_closing_balance(workers):
    CB = 0  # Closing Balance
    for worker in workers:
        if worker.CCV != -1:
            CB += worker.CCV
    print_res('Closing Balance: ', CB)
    return CB
# endregion

# endregion

# region ========================= MAIN PART 2 =========================

# region <!--- Part 1 Fair value of plan assets opening balance ---!>
# endregion


# region <!--- Part 2 Expected return on plan assets ---!>
def calculate_expected_return(worker, FVP_OB_VAR, discount_Rate, deposit_to_plan, benefits_paid):
    """
    This function calculates for !one! worker.
    :param worker: current one worker
    :param FVP_OB_VAR: Fair value of plan assets opening balance
    :param discount_Rate: Discount Rate
    :param deposit_to_plan: Deposits to plan
    :param benefits_paid: Benefits Paid
    """
    FVP_OB, DR, DP, BP = symbols('Fair_Value Discount_Rate Deposits_To_Plan Benefits_Paid')
    eq = FVP_OB * DR + ((DP - BP) * (DR / 2))

    eq_dict = {
        # TODO define FVP_OB = ???
        DR: discount_Rate,
        DP: deposit_to_plan,
        BP: benefits_paid
    }

    res = eq.subs(eq_dict)
    print_res('Calculated expected return for one employee: ', res)

    return res
# endregion


# region <!--- Part 3 Deposits to plan assets ---!>
# TODO sum all deposits for all the workers
# endregion


# region <!--- Part 4 Benefits paid from plan assets ---!>
# TODO sum all the benefits that been paid to workers that left
# endregion


# region <!--- Part 5 Actuarial gains (losses) ---!>
def calculate_actuarial_gains(FVP_CB, FVP_OB, ERPS, DPA, BP):
    """
    :param FVP_CB: Fair value of plan assets closing balance
    :param FVP_OB: Fair value of plan assets opening balance
    :param ERPS: Expected return on plan assets
    :param DPA: Deposits to plan assets
    :param BP: Benefits Paid
    """
    res = FVP_CB - FVP_OB - ERPS - DPA + BP
    print_res('Calculated Actuarial Gains: ', res)
    return res
# endregion


# region <!--- Part 6 Fair value of plan assets closing balance ---!>
# TODO sum all the assets for all the employees
# endregion
