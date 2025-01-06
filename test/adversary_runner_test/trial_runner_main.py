import unittest
from unittest.mock import patch
import queue
import threading
from threading import Event
import sys

sys.path.insert(0, './src')


from trial_runner.trial_runner_main import back_end_main_loop, run_adversarial_trial

class trial_runner_main_tests(unittest.TestCase):
    # test that passing a different model name to the function causes the corresponding model to be returned 



    @patch('trial_runner.trial_runner_main.run_adversarial_trial')
    def test_queues_updated_and_loop_triggered_once(self,mock_run_adversarial_trial):
        iteration_size = 5
        iteration_number = 1
        selected_attack = [None]
        selected_model = [None]
        hyperparameter_settings = [[]]
        image_queue = queue.Queue()
        graph_queue = queue.Queue()
        progress_bar_queue = queue.Queue()
        thread_killing_event = Event()
        back_end_main_loop(iteration_size,iteration_number,selected_attack,selected_model,hyperparameter_settings,image_queue,graph_queue,progress_bar_queue,thread_killing_event)
        self.assertEqual(image_queue.qsize(), 1)
        self.assertEqual(graph_queue.qsize(), 1)
        self.assertEqual(progress_bar_queue.qsize(), 1)
        self.assertEqual(mock_run_adversarial_trial.call_count,1)

    #def test_queues_updated_and_loop_triggered_multiple_times(self):

    #def test_hyper_parameter_normal_parsing(self):

    #def test_hyper_parameter_empty_parsing(self):

    #def test_hyper_parameter_repeat_parsing(self):

    #def test_results_directory_created_correctly(self):

    #def test_breaking_upon_event_setting:
        





if __name__ == '__main__':
    unittest.main()