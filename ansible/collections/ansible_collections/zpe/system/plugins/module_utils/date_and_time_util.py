def get_module_params():
    module_args = dict(
        date_and_time=dict(type='str', choices=['manual', 'network_time_protocol'], required=False, default='network_time_protocol'),
        server=dict(type='str', required=False, default='pool.ntp.org'),
        month=dict(type='str', choices=['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12'], required=False),
        day=dict(type='str', choices=['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '13', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31'], required=False),
        year=dict(type='str', choices=['2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025', '2026', '2027', '2028', '2029', '2030', '2031', '2032', '2033', '2034', '2035', '2036', '2037'], required=False),
        hour=dict(type='str', choices=['00', '01','02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23'], required=False),
        minute=dict(type='str', choices=['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51', '52', '53', '54', '55', '56', '57', '58', '59'], required=False),
        second=dict(type='str', choices=['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51', '52', '53', '54', '55', '56', '57', '58', '59'], required=False),
        zone=dict(type='str', choices=['africa|lagos', 'africa|nairobi', 'america|buenos_aires', 'america|edmonton', 'america|halifax', 'america|mexico_city', 'america|regina', 'america|sao_paulo', 'america|toronto', 'america|vancouver', 'utc+5:30', 'asia|dubai', 'asia|hong_kong', 'asia|seoul', 'asia|shanghai', 'asia|singapore', 'asia|taipei', 'asia|tokyo', 'australia|adelaide', 'australia|brisbane', 'australia|darwin', 'australia|eucla', 'australia|lord_howe', 'australia|perth', 'australia|sydney', 'europe|berlin', 'europe|lisbon', 'europe|london', 'europe|moscow', 'europe|paris', 'europe|sofia', 'gmt', 'utc-1', 'utc-10', 'utc-11', 'utc-12', 'utc-2', 'utc-3', 'utc-4', 'utc-5', 'utc-6', 'utc-7', 'utc-8', 'utc-9', 'utc+1', 'utc+10', 'utc+11', 'utc+12', 'utc+2', 'utc+3', 'utc+4', 'utc+5', 'utc+6', 'utc+7', 'utc+8', 'utc+9', 'gmt0', 'us|alaska', 'us|central', 'us|eastern', 'us|hawaii', 'us|mountain', 'us|pacific', 'utc'], required=False, default='utc'),
        enable_date_and_time_synchronization=dict(type='str', choices=['no','yes'], required=False, default='no'),
    )
    return module_args

def get_nodegrid_dict():
    nodegrid_keys = dict(
        date_and_time=dict(
            ansible_name="date_and_time",
            cli_name="date_and_time",
            cli_default="network_time_protocol",
            parent=False,
            parent_ansible_name="",
            parent_value=[''],
            import_template="/settings/date_and_time/ {cli_name}={value}"
        ),
        server=dict(
            ansible_name="server",
            cli_name="server",
            cli_default="pool.ntp.org",
            parent=False,
            parent_ansible_name="date_and_time",
            parent_value=[''],
            import_template="/settings/date_and_time/ {cli_name}={value}"
        ),
        month=dict(
            ansible_name="month",
            cli_name="month",
            cli_default="",
            parent=True,
            parent_ansible_name="date_and_time",
            parent_value=['manual'],
            import_template="/settings/date_and_time/ {cli_name}={value}"
        ),
        day=dict(
            ansible_name="day",
            cli_name="day",
            cli_default="",
            parent=True,
            parent_ansible_name="date_and_time",
            parent_value=['manual'],
            import_template="/settings/date_and_time/ {cli_name}={value}"
        ),
        year=dict(
            ansible_name="year",
            cli_name="year",
            cli_default="",
            parent=True,
            parent_ansible_name="date_and_time",
            parent_value=['manual'],
            import_template="/settings/date_and_time/ {cli_name}={value}"
        ),
        hour=dict(
            ansible_name="hour",
            cli_name="hour",
            cli_default="",
            parent=True,
            parent_ansible_name="date_and_time",
            parent_value=['manual'],
            import_template="/settings/date_and_time/ {cli_name}={value}"
        ),
        minute=dict(
            ansible_name="minute",
            cli_name="minute",
            cli_default="",
            parent=True,
            parent_ansible_name="date_and_time",
            parent_value=['manual'],
            import_template="/settings/date_and_time/ {cli_name}={value}"
        ),
        second=dict(
            ansible_name="second",
            cli_name="second",
            cli_default="",
            parent=True,
            parent_ansible_name="date_and_time",
            parent_value=['manual'],
            import_template="/settings/date_and_time/ {cli_name}={value}"
        ),
        zone=dict(
            ansible_name="zone",
            cli_name="zone",
            cli_default="utc",
            parent=False,
            parent_ansible_name="",
            parent_value=[''],
            import_template="/settings/date_and_time/ {cli_name}={value}"
        ),
        enable_date_and_time_synchronization=dict(
            ansible_name="enable_date_and_time_synchronization",
            cli_name="enable_date_and_time_synchronization",
            cli_default="no",
            parent=False,
            parent_ansible_name="",
            parent_value=[''],
            import_template="/settings/date_and_time/ {cli_name}={value}"
        ),
    )
    return nodegrid_keys
