from BLL.automatic_filling_of_the_table import register_new_animal, measure_query_time

i = input("Кількість нових тварин: ")
register_new_animal(i)

measure_query_time()