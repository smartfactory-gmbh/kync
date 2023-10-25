from django.test import TestCase
from mixer.backend.django import mixer

from sync.models import Group, Person, PublicKey

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


EXPECTED_OUTPUT = """
########################################
# TEST GROUP
########################################

ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQCTUvmGrYlVjfhOiiV/znXeOLQan0sHACTNXwSDe6rmv2A8SLU3UMy3citXrvaFscIcB7s8bmiV4HHVGVtdOeeJT+PHAwcCPhWeso1tpQYYsCF5jTK1Ma4s53fvozvP/R8wkDis8gAO911jng6CShZ6WkkqpEoo67Ddm+4T4+WfYD36ktixh2Ozbqx+PU41J5ynaIhyO3JgRkd19AZVQhEknBayh5zXResycdMk1swjGmIhJjvthqYzA0meVVIEG1U+UZm1BvLMlF97aM6529gWtZk3xO3sCmDZncSYAxfiXQY3OTXj14zaPEDJ/T8wcwjluQ0lTb0jB25hzpG3PyBExbxIoSsOZJsyQYCJrzFE8EUyXUoxhwJshK1fDI3cEFAeF81Cd4MrYgkCRx8lSLDa4tYZDaP7j34KavhKOv/gm3oWvkeqELz1Lp9ApvZTPIVen6j8pUjuev8wXdKbuR3S4g6moxw+kC6GLJtWu0QM1nVB9JKege6eW9C7DW/w4m8= dummy@dummy-machine
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQCV/y6JMrMbTWfRCKXE2Qak3A14h+K1XBhIq3s+kDUXNxta68NV5iFLHQ8QdKmnlW1U7u14DXNDSsBon7Up0wVZlyA8xVW0XkikFqm6OUE00NH/RZbVRpx6cUdkGgxI+XoBfVMxgPAo5NQWqcoJSqSTjZIee8IVdDQMJ/soBqWUMYzdj0oes+lD4JYjN6eW1M6BBK/UYuq48PE0D/cP9LhQ3zghd8B1Pl4R29KvnL84b14+gDIhlxtiMMG3uE4CQ0npjUFqBLV3+R+yRgHMxfxmSggV8gf6VJBzQw06Jvw3yHvEJw0qTqZNeUxuRjzrwvmBqrSS+ViipD1AX+wel2fuxLgyfjjQN5kg+NufdviRq73KA9Ao/EJThRz1QeKeCcK9kKlJpnw0SLzQ4EuxIeonhsvLaj7JdpKDmZ+Fx2dGmiUs9E0P6B60fwMDQvvN4ztkrppUjW7o5xLGUn3ob0WlgJa97TSDxEJ1QU4vLcfrNB0g92Uj+rPsT7PKSTFE1sM= dummy@dummy-machine
ssh-rsa BAAAB3NzaC1yc2EAAAADAQABAAABgQCTUvmGrYlVjfhOiiV/znXeOLQan0sHACTNXwSDe6rmv2A8SLU3UMy3citXrvaFscIcB7s8bmiV4HHVGVtdOeeJT+PHAwcCPhWeso1tpQYYsCF5jTK1Ma4s53fvozvP/R8wkDis8gAO911jng6CShZ6WkkqpEoo67Ddm+4T4+WfYD36ktixh2Ozbqx+PU41J5ynaIhyO3JgRkd19AZVQhEknBayh5zXResycdMk1swjGmIhJjvthqYzA0meVVIEG1U+UZm1BvLMlF97aM6529gWtZk3xO3sCmDZncSYAxfiXQY3OTXj14zaPEDJ/T8wcwjluQ0lTb0jB25hzpG3PyBExbxIoSsOZJsyQYCJrzFE8EUyXUoxhwJshK1fDI3cEFAeF81Cd4MrYgkCRx8lSLDa4tYZDaP7j34KavhKOv/gm3oWvkeqELz1Lp9ApvZTPIVen6j8pUjuev8wXdKbuR3S4g6moxw+kC6GLJtWu0QM1nVB9JKege6eW9C7DW/w4m8= dummy2@dummy-machine
ssh-rsa BAAAB3NzaC1yc2EAAAADAQABAAABgQCV/y6JMrMbTWfRCKXE2Qak3A14h+K1XBhIq3s+kDUXNxta68NV5iFLHQ8QdKmnlW1U7u14DXNDSsBon7Up0wVZlyA8xVW0XkikFqm6OUE00NH/RZbVRpx6cUdkGgxI+XoBfVMxgPAo5NQWqcoJSqSTjZIee8IVdDQMJ/soBqWUMYzdj0oes+lD4JYjN6eW1M6BBK/UYuq48PE0D/cP9LhQ3zghd8B1Pl4R29KvnL84b14+gDIhlxtiMMG3uE4CQ0npjUFqBLV3+R+yRgHMxfxmSggV8gf6VJBzQw06Jvw3yHvEJw0qTqZNeUxuRjzrwvmBqrSS+ViipD1AX+wel2fuxLgyfjjQN5kg+NufdviRq73KA9Ao/EJThRz1QeKeCcK9kKlJpnw0SLzQ4EuxIeonhsvLaj7JdpKDmZ+Fx2dGmiUs9E0P6B60fwMDQvvN4ztkrppUjW7o5xLGUn3ob0WlgJa97TSDxEJ1QU4vLcfrNB0g92Uj+rPsT7PKSTFE1sM= dummy2@dummy-machine
""".strip()  # noqa

EXPECTED_OUTPUT_WITH_INACTIVE_USER = """
########################################
# TEST GROUP
########################################

ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQCTUvmGrYlVjfhOiiV/znXeOLQan0sHACTNXwSDe6rmv2A8SLU3UMy3citXrvaFscIcB7s8bmiV4HHVGVtdOeeJT+PHAwcCPhWeso1tpQYYsCF5jTK1Ma4s53fvozvP/R8wkDis8gAO911jng6CShZ6WkkqpEoo67Ddm+4T4+WfYD36ktixh2Ozbqx+PU41J5ynaIhyO3JgRkd19AZVQhEknBayh5zXResycdMk1swjGmIhJjvthqYzA0meVVIEG1U+UZm1BvLMlF97aM6529gWtZk3xO3sCmDZncSYAxfiXQY3OTXj14zaPEDJ/T8wcwjluQ0lTb0jB25hzpG3PyBExbxIoSsOZJsyQYCJrzFE8EUyXUoxhwJshK1fDI3cEFAeF81Cd4MrYgkCRx8lSLDa4tYZDaP7j34KavhKOv/gm3oWvkeqELz1Lp9ApvZTPIVen6j8pUjuev8wXdKbuR3S4g6moxw+kC6GLJtWu0QM1nVB9JKege6eW9C7DW/w4m8= dummy@dummy-machine
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQCV/y6JMrMbTWfRCKXE2Qak3A14h+K1XBhIq3s+kDUXNxta68NV5iFLHQ8QdKmnlW1U7u14DXNDSsBon7Up0wVZlyA8xVW0XkikFqm6OUE00NH/RZbVRpx6cUdkGgxI+XoBfVMxgPAo5NQWqcoJSqSTjZIee8IVdDQMJ/soBqWUMYzdj0oes+lD4JYjN6eW1M6BBK/UYuq48PE0D/cP9LhQ3zghd8B1Pl4R29KvnL84b14+gDIhlxtiMMG3uE4CQ0npjUFqBLV3+R+yRgHMxfxmSggV8gf6VJBzQw06Jvw3yHvEJw0qTqZNeUxuRjzrwvmBqrSS+ViipD1AX+wel2fuxLgyfjjQN5kg+NufdviRq73KA9Ao/EJThRz1QeKeCcK9kKlJpnw0SLzQ4EuxIeonhsvLaj7JdpKDmZ+Fx2dGmiUs9E0P6B60fwMDQvvN4ztkrppUjW7o5xLGUn3ob0WlgJa97TSDxEJ1QU4vLcfrNB0g92Uj+rPsT7PKSTFE1sM= dummy@dummy-machine
""".strip()  # noqa


class GroupModelTestCase(TestCase):
    def test_group_output(self):
        person: Person = mixer.blend(Person)
        mixer.cycle(2).blend(PublicKey, content=(key for key in DUMMY_PUBLIC_KEYS_PERSON_ONE), person=person)

        other_person: Person = mixer.blend(Person)
        mixer.cycle(2).blend(PublicKey, content=(key for key in DUMMY_PUBLIC_KEYS_PERSON_TWO), person=other_person)

        group: Group = mixer.blend(Group, name="Test group")

        group.persons.add(person)
        group.persons.add(other_person)

        self.assertEqual(group.output, EXPECTED_OUTPUT)

        other_person.active = False
        other_person.save()
        self.assertEqual(group.output, EXPECTED_OUTPUT_WITH_INACTIVE_USER)
