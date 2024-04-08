def precision(plagiarism_detected, real_plagiarism):
    plagiarism_detected_count = len(plagiarism_detected) if len(plagiarism_detected) > 0 else 1e-10
    return len(set(plagiarism_detected) & set(real_plagiarism)) / plagiarism_detected_count


def recall(plagiarism_detected, real_plagiarism):
    tp = len(set(plagiarism_detected) & set(real_plagiarism))
    return tp / (tp + len(set(plagiarism_detected).difference(set(real_plagiarism)))) or 1e-10


def f(plagiarism_detected, real_plagiarism, beta):
    denominator = (beta ** 2 * precision(plagiarism_detected, real_plagiarism) + recall(plagiarism_detected,
                                                                                                  real_plagiarism))
    return (1 + beta ** 2) * precision(plagiarism_detected, real_plagiarism) * recall(
        plagiarism_detected, real_plagiarism) / denominator if denominator > 0 else 1e-10


def f1(plagiarism_detected, real_plagiarism):
    return f(plagiarism_detected, real_plagiarism, 1)


def fallout(plagiarism_detected, real_plagiarism, all_tests):
    fp = len(set(plagiarism_detected).difference(set(real_plagiarism)))
    tn = len(set(all_tests).difference(
        set(plagiarism_detected).union(set(real_plagiarism))))
    return fp / (fp + tn) if fp + tn > 0 else 1e-10


def get_evaluation(all_tests, real_plagiarism, plagiarism_detected):
    return {
        "precision": precision(plagiarism_detected, real_plagiarism),
        "recall": recall(plagiarism_detected, real_plagiarism),
        "f1": f1(plagiarism_detected, real_plagiarism),
        "fallout": fallout(plagiarism_detected, real_plagiarism, all_tests)
    }
