

class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self, training_type, duration, distance, speed, calories):
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self):
        """Возвращает строку информационного сообщения."""
        MESSAGE = ('Тип тренировки: {sport}; '
                   'Длительность: {time:.3f} ч.; '
                   'Дистанция: {dist:.3f} км; '
                   'Ср. скорость: {spe:.3f} км/ч; '
                   'Потрачено ккал: {cal:.3f}.')
        return (MESSAGE.format(sport=self.training_type,
                               time=self.duration,
                               dist=self.distance,
                               spe=self.speed,
                               cal=self.calories))


class Training:
    """Базовый класс тренировки."""

    LEN_STEP = 0.65
    M_IN_KM = 1000
    MIN_IN_HOUR = 60

    def __init__(self, action: int, duration: float, weight: float):
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self):
        """Получить дистанцию в км."""
        LEN_STEP = 0.65
        M_IN_KM = 1000
        return (self.action * LEN_STEP) / M_IN_KM

    def get_mean_speed(self):
        """Получить среднюю скорость движения."""
        distance = Training.get_distance(self)
        return distance / self.duration

    def get_spent_calories(self):
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self):
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed,
                           self.get_spent_calories)


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79
    M_IN_KM = 1000

    def get_spent_calories(self):
        """Реализация расчета калорий для бега."""

        calories = ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                     * self.get_mean_speed()
                     + self.CALORIES_MEAN_SPEED_SHIFT)
                    * self.weight / self.M_IN_KM
                    * (self.duration * self.MIN_IN_HOUR))
        return calories

    def show_training_info(self):
        """Вернуть информационное сообщение о выполненной тренировке."""
        distance = self.get_distance()
        speed = self.get_mean_speed()
        calories = self.get_spent_calories()
        return InfoMessage(self.__class__.__name__, self.duration, distance,
                           speed, calories)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_WEIGHT_COEFFICIENT = 0.035
    CALORIES_SPEED_COEFFICIENT = 0.029
    M_IN_KM = 1000
    SECONDS_IN_HOUR = 0.278  # Добавляем константу для секунд в часе
    METERS = 100

    def __init__(self, action: int, duration: float, weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self):
        """Реализация расчета калорий для спортивной ходьбы."""

        calories = ((self.CALORIES_WEIGHT_COEFFICIENT * self.weight
                     + ((self.get_mean_speed() * self.SECONDS_IN_HOUR) ** 2
                        / (self.height / self.METERS))
                     * self.CALORIES_SPEED_COEFFICIENT * self.weight)
                    * (self.duration * self.MIN_IN_HOUR))
        return calories

    def show_training_info(self):
        """Вернуть информационное сообщение о выполненной тренировке."""
        distance = self.get_distance()
        speed = self.get_mean_speed()
        calories = self.get_spent_calories()
        return InfoMessage(self.__class__.__name__, self.duration, distance,
                           speed,
                           calories)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38  # Длина гребка в метрах
    CALORIES_MEAN_SPEED_SHIFT = 1.1
    SPEED_MULTIPLIER = 2

    def __init__(self, action: int, duration: float, weight: float,
                 length_pool: float, count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self):
        """Реализация расчета средней скорости для плавания."""
        M_IN_KM = 1000
        mean_speed = ((self.length_pool * self.count_pool / M_IN_KM)
                      / self.duration)
        return mean_speed

    def get_spent_calories(self):
        """Реализация расчета калорий для плавания."""
        mean_speed = self.get_mean_speed()
        calories = ((mean_speed + self.CALORIES_MEAN_SPEED_SHIFT)
                    * self.SPEED_MULTIPLIER
                    * self.weight * self.duration)
        return calories

    def show_training_info(self):
        """Вернуть информационное сообщение о выполненной тренировке."""
        distance = self.get_distance()
        speed = self.get_mean_speed()
        calories = self.get_spent_calories()
        return InfoMessage(self.__class__.__name__, self.duration, distance,
                           speed, calories)


def read_package(workout_type: str, data: list[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_classes = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking,
    }

    train = workout_classes[workout_type]
    return train(*data)


def main(training: Training) -> None:
    """Главная функция."""

    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
