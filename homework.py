class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float):
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (
            f"Тип тренировки: {self.training_type}; "
            f"Длительность: {self.duration:.3f} ч.; "
            f"Дистанция: {self.distance:.3f} км; "
            f"Ср. скорость: {self.speed:.3f} км/ч; "
            f"Калории: {self.calories:.3f} ккал")


class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    M_IN_KM = 1000
    HOURS_TO_MINUTES = 60
    CM_TO_M = 0.01  # Add this constant

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return (self.action * self.LEN_STEP) / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        training_type = type(self).__name__
        duration = self.duration
        distance = self.get_distance()
        speed = self.get_mean_speed()
        calories = self.get_spent_calories()
        return InfoMessage(training_type, duration, distance, speed, calories)


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def get_spent_calories(self) -> float:
        """Переопределение метода для расчета калорий при беге."""
        duration_minutes = self.duration * Training.HOURS_TO_MINUTES
        calories = (
            (self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
             + self.CALORIES_MEAN_SPEED_SHIFT)
            * self.weight / self.M_IN_KM * duration_minutes
        )
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_WEIGHT_COEFF = 0.035
    CALORIES_SPEED_COEFF = 0.029
    KM_PER = 0.278  # Add this constant

    def __init__(self, action: int, duration: float, weight: float,
                 height: float):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Переопределение метода для расчета калорий при спортивной ходьбе."""
        duration_minutes = self.duration * Training.HOURS_TO_MINUTES
        speed_mps = self.get_mean_speed() * SportsWalking.KM_PER
        calories = (
            (self.CALORIES_WEIGHT_COEFF * self.weight
             + (speed_mps ** 2 / (self.height * Training.CM_TO_M))
             * self.CALORIES_SPEED_COEFF * self.weight)
            * duration_minutes
        )
        return calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    CALORIES_HEIGHT_COEFF = 1.1

    def __init__(self, action: int, duration: float, weight: float,
                 length_pool: float, count_pool: int):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Переопределение метода для расчета средней скорости при плавании."""
        duration_minutes = self.duration * Training.HOURS_TO_MINUTES
        return ((self.length_pool * self.count_pool
                 * Training.CM_TO_M / self.M_IN_KM)
                / duration_minutes)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_classes = {
        'RUN': Running,
        'WLK': SportsWalking,
        'SWM': Swimming
    }

    workout_class = workout_classes.get(workout_type)

    if workout_class:
        if workout_type == 'SWM':
            action, duration, weight, length_pool, count_pool = data
            return workout_class(action, duration, weight, length_pool,
                                 count_pool)
        else:
            action, duration, weight = data
            return workout_class(action, duration, weight)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    message = info.get_message()
    print(message)


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
