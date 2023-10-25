from typing import List
from unittest import mock

from django.test import TestCase, override_settings
from mixer.backend.django import mixer

from sync.models import Environment, Group, Person, Project, PublicKey

DUMMY_PUBLIC_KEYS_PERSON_ONE = [  # noqa
    (
        "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQCTUvmGrYlVjfhOiiV/znXeOLQan0sHACTNXwSDe6rmv2A8SLU3UMy3citXrvaFscIcB7s8b"
        "miV4HHVGVtdOeeJT+PHAwcCPhWeso1tpQYYsCF5jTK1Ma4s53fvozvP/R8wkDis8gAO911jng6CShZ6WkkqpEoo67Ddm+4T4+WfYD36ktixh2"
        "Ozbqx+PU41J5ynaIhyO3JgRkd19AZVQhEknBayh5zXResycdMk1swjGmIhJjvthqYzA0meVVIEG1U+UZm1BvLMlF97aM6529gWtZk3xO3sCmD"
        "ZncSYAxfiXQY3OTXj14zaPEDJ/T8wcwjluQ0lTb0jB25hzpG3PyBExbxIoSsOZJsyQYCJrzFE8EUyXUoxhwJshK1fDI3cEFAeF81Cd4MrYgkC"
        "Rx8lSLDa4tYZDaP7j34KavhKOv/gm3oWvkeqELz1Lp9ApvZTPIVen6j8pUjuev8wXdKbuR3S4g6moxw+kC6GLJtWu0QM1nVB9JKege6eW9C7D"
        "W/w4m8= dummy@dummy-machine"
    ),
    (
        "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQCV/y6JMrMbTWfRCKXE2Qak3A14h+K1XBhIq3s+kDUXNxta68NV5iFLHQ8QdKmnlW1U7u14D"
        "XNDSsBon7Up0wVZlyA8xVW0XkikFqm6OUE00NH/RZbVRpx6cUdkGgxI+XoBfVMxgPAo5NQWqcoJSqSTjZIee8IVdDQMJ/soBqWUMYzdj0oes+"
        "lD4JYjN6eW1M6BBK/UYuq48PE0D/cP9LhQ3zghd8B1Pl4R29KvnL84b14+gDIhlxtiMMG3uE4CQ0npjUFqBLV3+R+yRgHMxfxmSggV8gf6VJB"
        "zQw06Jvw3yHvEJw0qTqZNeUxuRjzrwvmBqrSS+ViipD1AX+wel2fuxLgyfjjQN5kg+NufdviRq73KA9Ao/EJThRz1QeKeCcK9kKlJpnw0SLzQ"
        "4EuxIeonhsvLaj7JdpKDmZ+Fx2dGmiUs9E0P6B60fwMDQvvN4ztkrppUjW7o5xLGUn3ob0WlgJa97TSDxEJ1QU4vLcfrNB0g92Uj+rPsT7PKS"
        "TFE1sM= dummy@dummy-machine"
    ),
]

DUMMY_PUBLIC_KEYS_PERSON_TWO = [  # noqa
    (
        "ssh-rsa BAAAB3NzaC1yc2EAAAADAQABAAABgQCTUvmGrYlVjfhOiiV/znXeOLQan0sHACTNXwSDe6rmv2A8SLU3UMy3citXrvaFscIcB7s8b"
        "miV4HHVGVtdOeeJT+PHAwcCPhWeso1tpQYYsCF5jTK1Ma4s53fvozvP/R8wkDis8gAO911jng6CShZ6WkkqpEoo67Ddm+4T4+WfYD36ktixh2"
        "Ozbqx+PU41J5ynaIhyO3JgRkd19AZVQhEknBayh5zXResycdMk1swjGmIhJjvthqYzA0meVVIEG1U+UZm1BvLMlF97aM6529gWtZk3xO3sCmD"
        "ZncSYAxfiXQY3OTXj14zaPEDJ/T8wcwjluQ0lTb0jB25hzpG3PyBExbxIoSsOZJsyQYCJrzFE8EUyXUoxhwJshK1fDI3cEFAeF81Cd4MrYgkC"
        "Rx8lSLDa4tYZDaP7j34KavhKOv/gm3oWvkeqELz1Lp9ApvZTPIVen6j8pUjuev8wXdKbuR3S4g6moxw+kC6GLJtWu0QM1nVB9JKege6eW9C7D"
        "W/w4m8= dummy2@dummy-machine"
    ),
    (
        "ssh-rsa BAAAB3NzaC1yc2EAAAADAQABAAABgQCV/y6JMrMbTWfRCKXE2Qak3A14h+K1XBhIq3s+kDUXNxta68NV5iFLHQ8QdKmnlW1U7u14D"
        "XNDSsBon7Up0wVZlyA8xVW0XkikFqm6OUE00NH/RZbVRpx6cUdkGgxI+XoBfVMxgPAo5NQWqcoJSqSTjZIee8IVdDQMJ/soBqWUMYzdj0oes+"
        "lD4JYjN6eW1M6BBK/UYuq48PE0D/cP9LhQ3zghd8B1Pl4R29KvnL84b14+gDIhlxtiMMG3uE4CQ0npjUFqBLV3+R+yRgHMxfxmSggV8gf6VJB"
        "zQw06Jvw3yHvEJw0qTqZNeUxuRjzrwvmBqrSS+ViipD1AX+wel2fuxLgyfjjQN5kg+NufdviRq73KA9Ao/EJThRz1QeKeCcK9kKlJpnw0SLzQ"
        "4EuxIeonhsvLaj7JdpKDmZ+Fx2dGmiUs9E0P6B60fwMDQvvN4ztkrppUjW7o5xLGUn3ob0WlgJa97TSDxEJ1QU4vLcfrNB0g92Uj+rPsT7PKS"
        "TFE1sM= dummy2@dummy-machine"
    ),
]


EXPECTED_OUTPUT_FULL = """
#  888    d8P
#  888   d8P
#  888  d8P
#  888d88K     888  888 88888b.   .d8888b
#  8888888b    888  888 888 "88b d88P"
#  888  Y88b   888  888 888  888 888
#  888   Y88b  Y88b 888 888  888 Y88b.
#  888    Y88b  "Y88888 888  888  "Y8888P
#                   888
#              Y8b d88P
#               "Y88P"

# Project name: Test project
# Host: test.non-existent.smf.ai
# Environment: test environment

ssh-rsa BAAAB3NzaC1yc2EAAAADAQABAAABgQCTUvmGrYlVjfhOiiV/znXeOLQan0sHACTNXwSDe6rmv2A8SLU3UMy3citXrvaFscIcB7s8bmiV4HHVGVtdOeeJT+PHAwcCPhWeso1tpQYYsCF5jTK1Ma4s53fvozvP/R8wkDis8gAO911jng6CShZ6WkkqpEoo67Ddm+4T4+WfYD36ktixh2Ozbqx+PU41J5ynaIhyO3JgRkd19AZVQhEknBayh5zXResycdMk1swjGmIhJjvthqYzA0meVVIEG1U+UZm1BvLMlF97aM6529gWtZk3xO3sCmDZncSYAxfiXQY3OTXj14zaPEDJ/T8wcwjluQ0lTb0jB25hzpG3PyBExbxIoSsOZJsyQYCJrzFE8EUyXUoxhwJshK1fDI3cEFAeF81Cd4MrYgkCRx8lSLDa4tYZDaP7j34KavhKOv/gm3oWvkeqELz1Lp9ApvZTPIVen6j8pUjuev8wXdKbuR3S4g6moxw+kC6GLJtWu0QM1nVB9JKege6eW9C7DW/w4m8= dummy2@dummy-machine
ssh-rsa BAAAB3NzaC1yc2EAAAADAQABAAABgQCV/y6JMrMbTWfRCKXE2Qak3A14h+K1XBhIq3s+kDUXNxta68NV5iFLHQ8QdKmnlW1U7u14DXNDSsBon7Up0wVZlyA8xVW0XkikFqm6OUE00NH/RZbVRpx6cUdkGgxI+XoBfVMxgPAo5NQWqcoJSqSTjZIee8IVdDQMJ/soBqWUMYzdj0oes+lD4JYjN6eW1M6BBK/UYuq48PE0D/cP9LhQ3zghd8B1Pl4R29KvnL84b14+gDIhlxtiMMG3uE4CQ0npjUFqBLV3+R+yRgHMxfxmSggV8gf6VJBzQw06Jvw3yHvEJw0qTqZNeUxuRjzrwvmBqrSS+ViipD1AX+wel2fuxLgyfjjQN5kg+NufdviRq73KA9Ao/EJThRz1QeKeCcK9kKlJpnw0SLzQ4EuxIeonhsvLaj7JdpKDmZ+Fx2dGmiUs9E0P6B60fwMDQvvN4ztkrppUjW7o5xLGUn3ob0WlgJa97TSDxEJ1QU4vLcfrNB0g92Uj+rPsT7PKSTFE1sM= dummy2@dummy-machine

########################################
# TEST GROUP
########################################

ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQCTUvmGrYlVjfhOiiV/znXeOLQan0sHACTNXwSDe6rmv2A8SLU3UMy3citXrvaFscIcB7s8bmiV4HHVGVtdOeeJT+PHAwcCPhWeso1tpQYYsCF5jTK1Ma4s53fvozvP/R8wkDis8gAO911jng6CShZ6WkkqpEoo67Ddm+4T4+WfYD36ktixh2Ozbqx+PU41J5ynaIhyO3JgRkd19AZVQhEknBayh5zXResycdMk1swjGmIhJjvthqYzA0meVVIEG1U+UZm1BvLMlF97aM6529gWtZk3xO3sCmDZncSYAxfiXQY3OTXj14zaPEDJ/T8wcwjluQ0lTb0jB25hzpG3PyBExbxIoSsOZJsyQYCJrzFE8EUyXUoxhwJshK1fDI3cEFAeF81Cd4MrYgkCRx8lSLDa4tYZDaP7j34KavhKOv/gm3oWvkeqELz1Lp9ApvZTPIVen6j8pUjuev8wXdKbuR3S4g6moxw+kC6GLJtWu0QM1nVB9JKege6eW9C7DW/w4m8= dummy@dummy-machine
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQCV/y6JMrMbTWfRCKXE2Qak3A14h+K1XBhIq3s+kDUXNxta68NV5iFLHQ8QdKmnlW1U7u14DXNDSsBon7Up0wVZlyA8xVW0XkikFqm6OUE00NH/RZbVRpx6cUdkGgxI+XoBfVMxgPAo5NQWqcoJSqSTjZIee8IVdDQMJ/soBqWUMYzdj0oes+lD4JYjN6eW1M6BBK/UYuq48PE0D/cP9LhQ3zghd8B1Pl4R29KvnL84b14+gDIhlxtiMMG3uE4CQ0npjUFqBLV3+R+yRgHMxfxmSggV8gf6VJBzQw06Jvw3yHvEJw0qTqZNeUxuRjzrwvmBqrSS+ViipD1AX+wel2fuxLgyfjjQN5kg+NufdviRq73KA9Ao/EJThRz1QeKeCcK9kKlJpnw0SLzQ4EuxIeonhsvLaj7JdpKDmZ+Fx2dGmiUs9E0P6B60fwMDQvvN4ztkrppUjW7o5xLGUn3ob0WlgJa97TSDxEJ1QU4vLcfrNB0g92Uj+rPsT7PKSTFE1sM= dummy@dummy-machine

# Kync key (always included)
############################

the-kync-key
""".lstrip()  # noqa

EXPECTED_OUTPUT_WITH_COMMENT = """
#  888    d8P
#  888   d8P
#  888  d8P
#  888d88K     888  888 88888b.   .d8888b
#  8888888b    888  888 888 "88b d88P"
#  888  Y88b   888  888 888  888 888
#  888   Y88b  Y88b 888 888  888 Y88b.
#  888    Y88b  "Y88888 888  888  "Y8888P
#                   888
#              Y8b d88P
#               "Y88P"

# Project name: Test project
# Host: test.non-existent.smf.ai
# Environment: test environment
# Comment: this is a comment

ssh-rsa BAAAB3NzaC1yc2EAAAADAQABAAABgQCTUvmGrYlVjfhOiiV/znXeOLQan0sHACTNXwSDe6rmv2A8SLU3UMy3citXrvaFscIcB7s8bmiV4HHVGVtdOeeJT+PHAwcCPhWeso1tpQYYsCF5jTK1Ma4s53fvozvP/R8wkDis8gAO911jng6CShZ6WkkqpEoo67Ddm+4T4+WfYD36ktixh2Ozbqx+PU41J5ynaIhyO3JgRkd19AZVQhEknBayh5zXResycdMk1swjGmIhJjvthqYzA0meVVIEG1U+UZm1BvLMlF97aM6529gWtZk3xO3sCmDZncSYAxfiXQY3OTXj14zaPEDJ/T8wcwjluQ0lTb0jB25hzpG3PyBExbxIoSsOZJsyQYCJrzFE8EUyXUoxhwJshK1fDI3cEFAeF81Cd4MrYgkCRx8lSLDa4tYZDaP7j34KavhKOv/gm3oWvkeqELz1Lp9ApvZTPIVen6j8pUjuev8wXdKbuR3S4g6moxw+kC6GLJtWu0QM1nVB9JKege6eW9C7DW/w4m8= dummy2@dummy-machine
ssh-rsa BAAAB3NzaC1yc2EAAAADAQABAAABgQCV/y6JMrMbTWfRCKXE2Qak3A14h+K1XBhIq3s+kDUXNxta68NV5iFLHQ8QdKmnlW1U7u14DXNDSsBon7Up0wVZlyA8xVW0XkikFqm6OUE00NH/RZbVRpx6cUdkGgxI+XoBfVMxgPAo5NQWqcoJSqSTjZIee8IVdDQMJ/soBqWUMYzdj0oes+lD4JYjN6eW1M6BBK/UYuq48PE0D/cP9LhQ3zghd8B1Pl4R29KvnL84b14+gDIhlxtiMMG3uE4CQ0npjUFqBLV3+R+yRgHMxfxmSggV8gf6VJBzQw06Jvw3yHvEJw0qTqZNeUxuRjzrwvmBqrSS+ViipD1AX+wel2fuxLgyfjjQN5kg+NufdviRq73KA9Ao/EJThRz1QeKeCcK9kKlJpnw0SLzQ4EuxIeonhsvLaj7JdpKDmZ+Fx2dGmiUs9E0P6B60fwMDQvvN4ztkrppUjW7o5xLGUn3ob0WlgJa97TSDxEJ1QU4vLcfrNB0g92Uj+rPsT7PKSTFE1sM= dummy2@dummy-machine

########################################
# TEST GROUP
########################################

ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQCTUvmGrYlVjfhOiiV/znXeOLQan0sHACTNXwSDe6rmv2A8SLU3UMy3citXrvaFscIcB7s8bmiV4HHVGVtdOeeJT+PHAwcCPhWeso1tpQYYsCF5jTK1Ma4s53fvozvP/R8wkDis8gAO911jng6CShZ6WkkqpEoo67Ddm+4T4+WfYD36ktixh2Ozbqx+PU41J5ynaIhyO3JgRkd19AZVQhEknBayh5zXResycdMk1swjGmIhJjvthqYzA0meVVIEG1U+UZm1BvLMlF97aM6529gWtZk3xO3sCmDZncSYAxfiXQY3OTXj14zaPEDJ/T8wcwjluQ0lTb0jB25hzpG3PyBExbxIoSsOZJsyQYCJrzFE8EUyXUoxhwJshK1fDI3cEFAeF81Cd4MrYgkCRx8lSLDa4tYZDaP7j34KavhKOv/gm3oWvkeqELz1Lp9ApvZTPIVen6j8pUjuev8wXdKbuR3S4g6moxw+kC6GLJtWu0QM1nVB9JKege6eW9C7DW/w4m8= dummy@dummy-machine
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQCV/y6JMrMbTWfRCKXE2Qak3A14h+K1XBhIq3s+kDUXNxta68NV5iFLHQ8QdKmnlW1U7u14DXNDSsBon7Up0wVZlyA8xVW0XkikFqm6OUE00NH/RZbVRpx6cUdkGgxI+XoBfVMxgPAo5NQWqcoJSqSTjZIee8IVdDQMJ/soBqWUMYzdj0oes+lD4JYjN6eW1M6BBK/UYuq48PE0D/cP9LhQ3zghd8B1Pl4R29KvnL84b14+gDIhlxtiMMG3uE4CQ0npjUFqBLV3+R+yRgHMxfxmSggV8gf6VJBzQw06Jvw3yHvEJw0qTqZNeUxuRjzrwvmBqrSS+ViipD1AX+wel2fuxLgyfjjQN5kg+NufdviRq73KA9Ao/EJThRz1QeKeCcK9kKlJpnw0SLzQ4EuxIeonhsvLaj7JdpKDmZ+Fx2dGmiUs9E0P6B60fwMDQvvN4ztkrppUjW7o5xLGUn3ob0WlgJa97TSDxEJ1QU4vLcfrNB0g92Uj+rPsT7PKSTFE1sM= dummy@dummy-machine

# Kync key (always included)
############################

the-kync-key
""".lstrip()  # noqa

EXPECTED_OUTPUT_WITH_DEACTIVATED_USER = """
#  888    d8P
#  888   d8P
#  888  d8P
#  888d88K     888  888 88888b.   .d8888b
#  8888888b    888  888 888 "88b d88P"
#  888  Y88b   888  888 888  888 888
#  888   Y88b  Y88b 888 888  888 Y88b.
#  888    Y88b  "Y88888 888  888  "Y8888P
#                   888
#              Y8b d88P
#               "Y88P"

# Project name: Test project
# Host: test.non-existent.smf.ai
# Environment: test environment

########################################
# TEST GROUP
########################################

ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQCTUvmGrYlVjfhOiiV/znXeOLQan0sHACTNXwSDe6rmv2A8SLU3UMy3citXrvaFscIcB7s8bmiV4HHVGVtdOeeJT+PHAwcCPhWeso1tpQYYsCF5jTK1Ma4s53fvozvP/R8wkDis8gAO911jng6CShZ6WkkqpEoo67Ddm+4T4+WfYD36ktixh2Ozbqx+PU41J5ynaIhyO3JgRkd19AZVQhEknBayh5zXResycdMk1swjGmIhJjvthqYzA0meVVIEG1U+UZm1BvLMlF97aM6529gWtZk3xO3sCmDZncSYAxfiXQY3OTXj14zaPEDJ/T8wcwjluQ0lTb0jB25hzpG3PyBExbxIoSsOZJsyQYCJrzFE8EUyXUoxhwJshK1fDI3cEFAeF81Cd4MrYgkCRx8lSLDa4tYZDaP7j34KavhKOv/gm3oWvkeqELz1Lp9ApvZTPIVen6j8pUjuev8wXdKbuR3S4g6moxw+kC6GLJtWu0QM1nVB9JKege6eW9C7DW/w4m8= dummy@dummy-machine
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQCV/y6JMrMbTWfRCKXE2Qak3A14h+K1XBhIq3s+kDUXNxta68NV5iFLHQ8QdKmnlW1U7u14DXNDSsBon7Up0wVZlyA8xVW0XkikFqm6OUE00NH/RZbVRpx6cUdkGgxI+XoBfVMxgPAo5NQWqcoJSqSTjZIee8IVdDQMJ/soBqWUMYzdj0oes+lD4JYjN6eW1M6BBK/UYuq48PE0D/cP9LhQ3zghd8B1Pl4R29KvnL84b14+gDIhlxtiMMG3uE4CQ0npjUFqBLV3+R+yRgHMxfxmSggV8gf6VJBzQw06Jvw3yHvEJw0qTqZNeUxuRjzrwvmBqrSS+ViipD1AX+wel2fuxLgyfjjQN5kg+NufdviRq73KA9Ao/EJThRz1QeKeCcK9kKlJpnw0SLzQ4EuxIeonhsvLaj7JdpKDmZ+Fx2dGmiUs9E0P6B60fwMDQvvN4ztkrppUjW7o5xLGUn3ob0WlgJa97TSDxEJ1QU4vLcfrNB0g92Uj+rPsT7PKSTFE1sM= dummy@dummy-machine

# Kync key (always included)
############################

the-kync-key
""".lstrip()  # noqa

EXPECTED_OUTPUT_WITH_DEACTIVATED_GROUP = """
#  888    d8P
#  888   d8P
#  888  d8P
#  888d88K     888  888 88888b.   .d8888b
#  8888888b    888  888 888 "88b d88P"
#  888  Y88b   888  888 888  888 888
#  888   Y88b  Y88b 888 888  888 Y88b.
#  888    Y88b  "Y88888 888  888  "Y8888P
#                   888
#              Y8b d88P
#               "Y88P"

# Project name: Test project
# Host: test.non-existent.smf.ai
# Environment: test environment

ssh-rsa BAAAB3NzaC1yc2EAAAADAQABAAABgQCTUvmGrYlVjfhOiiV/znXeOLQan0sHACTNXwSDe6rmv2A8SLU3UMy3citXrvaFscIcB7s8bmiV4HHVGVtdOeeJT+PHAwcCPhWeso1tpQYYsCF5jTK1Ma4s53fvozvP/R8wkDis8gAO911jng6CShZ6WkkqpEoo67Ddm+4T4+WfYD36ktixh2Ozbqx+PU41J5ynaIhyO3JgRkd19AZVQhEknBayh5zXResycdMk1swjGmIhJjvthqYzA0meVVIEG1U+UZm1BvLMlF97aM6529gWtZk3xO3sCmDZncSYAxfiXQY3OTXj14zaPEDJ/T8wcwjluQ0lTb0jB25hzpG3PyBExbxIoSsOZJsyQYCJrzFE8EUyXUoxhwJshK1fDI3cEFAeF81Cd4MrYgkCRx8lSLDa4tYZDaP7j34KavhKOv/gm3oWvkeqELz1Lp9ApvZTPIVen6j8pUjuev8wXdKbuR3S4g6moxw+kC6GLJtWu0QM1nVB9JKege6eW9C7DW/w4m8= dummy2@dummy-machine
ssh-rsa BAAAB3NzaC1yc2EAAAADAQABAAABgQCV/y6JMrMbTWfRCKXE2Qak3A14h+K1XBhIq3s+kDUXNxta68NV5iFLHQ8QdKmnlW1U7u14DXNDSsBon7Up0wVZlyA8xVW0XkikFqm6OUE00NH/RZbVRpx6cUdkGgxI+XoBfVMxgPAo5NQWqcoJSqSTjZIee8IVdDQMJ/soBqWUMYzdj0oes+lD4JYjN6eW1M6BBK/UYuq48PE0D/cP9LhQ3zghd8B1Pl4R29KvnL84b14+gDIhlxtiMMG3uE4CQ0npjUFqBLV3+R+yRgHMxfxmSggV8gf6VJBzQw06Jvw3yHvEJw0qTqZNeUxuRjzrwvmBqrSS+ViipD1AX+wel2fuxLgyfjjQN5kg+NufdviRq73KA9Ao/EJThRz1QeKeCcK9kKlJpnw0SLzQ4EuxIeonhsvLaj7JdpKDmZ+Fx2dGmiUs9E0P6B60fwMDQvvN4ztkrppUjW7o5xLGUn3ob0WlgJa97TSDxEJ1QU4vLcfrNB0g92Uj+rPsT7PKSTFE1sM= dummy2@dummy-machine

# Kync key (always included)
############################

the-kync-key
""".lstrip()  # noqa


@mock.patch.object(Environment, "sync_remote")
@mock.patch("sync.models.environment.get_kync_public_key", return_value="the-kync-key")
class EnvironmentModelTestCase(TestCase):
    def _create_environment(self) -> Environment:
        persons: List[Person] = mixer.cycle(2).blend(Person)
        mixer.cycle(2).blend(PublicKey, person=persons[0], content=(key for key in DUMMY_PUBLIC_KEYS_PERSON_ONE))
        mixer.cycle(2).blend(PublicKey, person=persons[1], content=(key for key in DUMMY_PUBLIC_KEYS_PERSON_TWO))

        group: Group = mixer.blend(Group, name="Test group")
        group.persons.add(persons[0])

        project: Project = mixer.blend(
            Project, name="Test project", ssh_user="test_user", host="test.non-existent.smf.ai"
        )

        project.groups.add(group)
        project.persons.add(persons[1])
        return mixer.blend(
            Environment,
            project=project,
            ssh_user="test_user",
            name="test environment",
            host="test.non-existent.smf.ai",
            comment="",
        )

    def test_environment_output_includes_both_groups_and_persons(
        self, _public_key_mock: mock.MagicMock, _sync_mock: mock.MagicMock
    ):
        environment = self._create_environment()
        self.assertEqual(environment.output, EXPECTED_OUTPUT_FULL)

    def test_environment_output_includes_comment(self, _public_key_mock: mock.MagicMock, _sync_mock: mock.MagicMock):
        environment = self._create_environment()
        environment.comment = "this is a comment"
        environment.internal_comment = "this should not get in the output"
        self.assertEqual(environment.output, EXPECTED_OUTPUT_WITH_COMMENT)

    def test_environment_output_exclude_deactivated_persons(
        self, _public_key_mock: mock.MagicMock, _sync_mock: mock.MagicMock
    ):
        environment = self._create_environment()

        person = environment.project.persons.first()
        person.active = False
        person.save()

        self.assertEqual(environment.output, EXPECTED_OUTPUT_WITH_DEACTIVATED_USER)

    def test_environment_output_exclude_deactivated_group(
        self, _public_key_mock: mock.MagicMock, _sync_mock: mock.MagicMock
    ):
        environment = self._create_environment()

        group = environment.project.groups.first()
        group.active = False
        group.save()

        self.assertEqual(environment.output, EXPECTED_OUTPUT_WITH_DEACTIVATED_GROUP)

    @override_settings(SSH_KEYPAIR_LOCATION="/some-location/.ssh", SSH_KEYPAIR_NAME="dummy")
    @mock.patch("sync.models.environment.SSHClient")
    def test_project_set_remote_authorized_keys_content(
        self, ssh_client_mock: mock.MagicMock, _sync_mock: mock.MagicMock, _public_key_mock: mock.MagicMock
    ):
        environment = self._create_environment()

        environment.write_authorized_keys()

        (
            ssh_client_mock.return_value.connect.assert_called_once_with(
                "test.non-existent.smf.ai", username="test_user", key_filename="/some-location/.ssh/dummy"
            )
        )

        (
            ssh_client_mock.return_value.open_sftp.return_value.file.assert_called_once_with(
                "/home/test_user/.ssh/authorized_keys", "w", -1
            )
        )

        (
            ssh_client_mock.return_value.open_sftp.return_value.file.return_value.write.assert_called_once_with(
                environment.output
            )
        )
