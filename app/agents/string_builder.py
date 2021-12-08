def string_builder(OR: str, AND: str, NOT: str) -> str:
    parm_not = NOT.split()
    parm_not = ['-' + c for c in parm_not]
    parm_not = ' '.join(parm_not)
    string = f'site:linkedin.com/in/ OR site:linkedin.com/pub/ ({OR}) {AND} {parm_not}'

    return string
