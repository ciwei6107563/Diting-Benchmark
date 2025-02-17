from .wer import judge as judge_wer
from .wer import judge_speechGPT as judge_wer_speechGPT
from .wer import judge__wer as judge__wer
from .wer import judge_chinese_wer
from .wer import judge_wer_find
from .knowledge import has_judge
from .yes_or_no.judge import is_true_yes_no as judge_yes_no
from .classifier.classifier import classifier_judge as judge_multiple_choice
if __name__ == '__main__':
    pass
