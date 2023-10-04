class InfoMessage:
    """Информационное сообщение о тренировке."""

    MESSAGE_TRANING = ('Тип тренировки: {sport}; '
                       'Длительность: {time:.3f} ч.; '
                       'Дистанция: {dist:.3f} км; '
                       'Ср. скорость: {spe:.3f} км/ч; '
                       'Потрачено ккал: {cal:.3f}.')

    def __init__(self, training_type: str, duration: float,
                 distance: float, speed: float, calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self):
        """Возвращает строку информационного сообщения."""
        return self.MESSAGE_TRANING.format(
            sport=self.training_type,
            time=self.duration,
            dist=self.distance,
            spe=self.speed,
            cal=self.calories
        )


class Training:
    """Базовый класс тренировки."""

    LEN_STEP = 0.65
    M_IN_KM = 1000
    MIN_IN_HOUR = 60

    def __init__(self, action: int, duration: float, weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self):
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self):
        """Получить среднюю скорость движения."""
        distance = self.get_distance()
        return distance / self.duration

    def get_spent_calories(self):
        """Получить количество затраченных калорий."""
        raise NotImplementedError("Метод реализован в дочерних классах")

    def show_training_info(self):
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def get_spent_calories(self):
        """Реализация расчета калорий для бега."""
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight / self.M_IN_KM
                * (self.duration * self.MIN_IN_HOUR))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    CALORIES_SPEED_MULTIPLIER = 0.029
    CALORIES_WEIGHT_MULTIPLIER = 0.035
    KM_PER_HOUR_TO_M_PER_SEC = 0.278    # Добавляем константу для секунд в часе
    CENTIMETERS_IN_METER = 100

    def __init__(self, action: int, duration: float, weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self):
        """Реализация расчета калорий для спортивной ходьбы."""

        return ((self.CALORIES_WEIGHT_MULTIPLIER * self.weight
                + ((self.get_mean_speed() * self.KM_PER_HOUR_TO_M_PER_SEC)
                 ** 2
                 / (self.height / self.CENTIMETERS_IN_METER))
                 * self.CALORIES_SPEED_MULTIPLIER * self.weight)
                * (self.duration * self.MIN_IN_HOUR))


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38  # Длина гребка в метрах
    CALORIES_MEAN_SPEED_SHIFT = 1.1
    CALORIES_MEAN_SPEED_MULTIPLIER = 2

    def __init__(self, action: int, duration: float, weight: float,
                 length_pool: float, count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self):
        """Реализация расчета средней скорости для плавания."""
        return ((self.length_pool * self.count_pool / self.M_IN_KM)
                / self.duration)

    def get_spent_calories(self):
        """Реализация расчета калорий для плавания."""
        return ((self.get_mean_speed() + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.CALORIES_MEAN_SPEED_MULTIPLIER
                * self.weight * self.duration)


WORKOUT_CLASSES: dict[str, type[Training]] = {
    'SWM': Swimming,
    'RUN': Running,
    'WLK': SportsWalking,
}


def read_package(workout_type: str, data: list[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    return WORKOUT_CLASSES[workout_type](*data)


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
