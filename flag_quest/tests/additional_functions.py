from flag_quest.models import Answer


def dummy_answers_creator(quantity_of_answers: int):
    for _ in range(quantity_of_answers):
        Answer.objects.create(
            flag_picture=f"test_flag_picture_{_}",
            is_correct=True,
            your_answer=f"correct_answer_{_}",
            correct_answer=f"correct_answer_{_}",
        )
