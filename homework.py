from typing import Any, Dict
from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        message: str = (f'Тип тренировки: {self.training_type}; '
                        f'Длительность: {self.duration:.3f} ч.; '
                        f'Дистанция: {self.distance:.3f} км; '
                        f'Ср. скорость: {self.speed:.3f} км/ч; '
                        f'Потрачено ккал: {self.calories:.3f}.')
        return message


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    TRAINING_TYPE: str = 'Training'

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float) -> None:
        self.action: int = action
        self.duration: float = duration
        self.weight: float = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance: float = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed: float = self.get_distance() / self.duration
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        training_type: str = self.TRAINING_TYPE
        duration: float = self.duration
        distance: float = self.get_distance()
        speed: float = self.get_mean_speed()
        calories: float = self.get_spent_calories()
        infomessage: InfoMessage = InfoMessage(training_type,
                                               duration,
                                               distance,
                                               speed,
                                               calories)
        return infomessage


class Running(Training):
    """Тренировка: бег."""
    coeff_calorie_1: int = 18
    coeff_calorie_2: int = 20
    TRAINING_TYPE: str = 'Running'

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        duration_in_minutes: float = self.duration * 60
        calories: float = ((self.coeff_calorie_1 * self.get_mean_speed()
                           - self.coeff_calorie_2) * self.weight
                           / self.M_IN_KM * duration_in_minutes)
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    coeff_calorie_1: float = 0.035
    coeff_calorie_2: float = 0.029
    TRAINING_TYPE: str = 'SportsWalking'

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height: float = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        duration_in_minutes: float = self.duration * 60
        calories: float = ((self.coeff_calorie_1 * self.weight
                           + (self.get_mean_speed()**2 // self.height)
                           * self.coeff_calorie_2 * self.weight)
                           * duration_in_minutes)
        return calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    coeff_calorie: float = 1.1
    TRAINING_TYPE: str = 'Swimming'

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float) -> None:
        super().__init__(action, duration, weight)
        self.length_pool: float = length_pool
        self.count_pool: float = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed: float = (self.length_pool * self.count_pool / self.M_IN_KM
                        / self.duration)
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        calories: float = ((self.get_mean_speed() + self.coeff_calorie)
                           * 2 * self.weight)
        return calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_dict: Dict[str, Any] = {'SWM': Swimming,
                                    'RUN': Running,
                                    'WLK': SportsWalking}
    training: Training = workout_dict[workout_type](*data)
    return training


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
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
