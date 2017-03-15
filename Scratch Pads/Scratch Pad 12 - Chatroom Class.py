

msg_type = "NORMAL"

# filter_dict = {0 : Server.ao_normal_msg,
#                1 : Server.ao_join_msg,
#                2 : Server.ao_user_msg,
#                3 : Server.ao_pass_msg,
#                4 : Server.ao_direct_msg,
#                5 : Server.ao_command_msg,
#                6 : Server.ao_server_msg}

# for key in filter_dict:
#     if key == msg_type:
#
#
# if msg_type in




filter_dict = {"NORMAL": 0,  # 0
         "JOIN": 1,  # 1
         "USER": 2,  # 2
         "PASS": 3,  # 3
         "DIRECT": 4,  # 4
         "COMMAND": 5,  # 5
         "SERVER": 6}  # 6


print(filter_dict[msg_type])