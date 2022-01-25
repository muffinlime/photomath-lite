import localization
import recognition
import solver


def full(image):
    localized = localization.localize(image)
    recognized = recognition.predict(localized)
    expression, result = solver.solver(recognized)
    return expression, result