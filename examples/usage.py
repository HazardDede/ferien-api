import ferien


# Get all vacations for all time and states
print("All vacations:", ferien.all_vacations())

# Get all vacations for a specific state (in this case Hamburg - HH) ...
print("All vacations for HH:", ferien.state_vacations('HH'))

# ... and optionally for a specific year
print("All vacations for HH in 2019:", ferien.state_vacations('HH', 2019))

# Fetch all valid states
print("Valid state codes:", ferien.state_codes())
