routing_graph = {
    '1': {'2': [2],
          '3': [1, 5],
          '5': [10]},
    '2': {'1': [1],
          '4': [3]},
    '3': {'6': [7],
          '1': [1]},
    '4': {'5': [5],
          '6': [4]},
    '5': {},
    '6': {'4': [4],
          '7': [9],
          '1': [2],
          '3': [7]},
    '7': {'6': [9]}
}

# dictionary used to restore waypoints from graph
# (1) -waypoint-> (2)
restore_graph = {
        '1': {'2': [1],
              '3': [2, 11],
              '5': [14]},
        '2': {'1': [3],
              '4': [4]},
        '3': {'6': [5],
              '1': [12]},
        '4': {'5': [6],
              '6': [7]},
        '5': {},
        '6': {'4': [8],
              '7': [9],
              '1': [13]},
        '7': {'6': [10]}
    }

waypoints = {
        1: {'cron': '0 * * * *', 'travel_time': 2, 'time_from_first_stop': 12, 'connection_id': 1},  # every hour
        2: {'cron': '0 0 * * *', 'travel_time': 1, 'time_from_first_stop': 34, 'connection_id': 2},  # every day at 00:00
        3: {'cron': '30 3 * * *', 'travel_time': 1, 'time_from_first_stop': 5, 'connection_id': 1},  # every day at 3:30 AM
        4: {'cron': '0 9 * * 1', 'travel_time': 3, 'time_from_first_stop': 21, 'connection_id': 1},  # every Monday at 9:00 AM
        5: {'cron': '*/15 * * * *', 'travel_time': 7, 'time_from_first_stop': 17, 'connection_id': 2},  # every 15 minutes
        6: {'cron': '30 8 * * 1-5', 'travel_time': 7, 'time_from_first_stop': 15, 'connection_id': 1},  # every weekday at 8:30 AM
        7: {'cron': '*/5 * * * *', 'travel_time': 4, 'time_from_first_stop': 7, 'connection_id': 4},  # every 5 seconds
        8: {'cron': '30 4 1 * *', 'travel_time': 4, 'time_from_first_stop': 0, 'connection_id': 4},  # every 1st of the month at 4:30 AM
        9: {'cron': '*/5 * * * 1-5', 'travel_time': 9, 'time_from_first_stop': 5, 'connection_id': 2},  # every 5 minutes on weekdays
        10: {'cron': '0 22 * * 6', 'travel_time': 9, 'time_from_first_stop': 12, 'connection_id': 2},  # every Saturday at 10:00 PM
        11: {'cron': '0 22 * * 6', 'travel_time': 5, 'time_from_first_stop': 20, 'connection_id': 3},  # every Saturday at 10:00 PM
        12: {'cron': '0 * * * *', 'travel_time': 2, 'time_from_first_stop': 23, 'connection_id': 2},  # every hour
        13: {'cron': '*/15 * * * *', 'travel_time': 7, 'time_from_first_stop': 12, 'connection_id': 5},  # every 15 minutes
        14: {'cron': '*/5 * * * 1-5', 'travel_time': 13, 'time_from_first_stop': 0, 'connection_id': 6}}  # every 5 minutes on weekdays
