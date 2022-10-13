def formatted_log(FILE_NAME, USERNAME, PASSWORD, AUTO_CONTINUE, AUTO_BOOKWORK, VERSION):
    return f"""[Auto Bookwork] By Acquite <3
[Start Time]: {FILE_NAME}
--- [Settings] --- 
    [Username]: {USERNAME}
    [Password]: {'*'*len(PASSWORD)}
    [Auto Continue]: {str(AUTO_CONTINUE)}
    [Auto Bookwork]: {str(AUTO_BOOKWORK)}
    [Version]: {VERSION}
--- [Work Logs] --- 
"""