import unittest
from unittest.mock import patch, call
import queue
import threading
from threading import Event
import sys
import os
import shutil
import threading
import time

sys.path.insert(0, './src')


from trial_runner.trial_runner_main import back_end_main_loop, run_adversarial_trial
from trial_runner.file_system_functions import update_cumulative_metrics

class trial_runner_main_tests(unittest.TestCase):
    # test that passing a different model name to the function causes the corresponding model to be returned 


    @patch('trial_runner.trial_runner_main.update_cumulative_metrics')
    @patch('trial_runner.trial_runner_main.run_adversarial_trial')
    def test_queues_updated_and_loop_triggered_once(self,mock_run_adversarial_trial,mock_update_cumulative_metrics):
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


    @patch('trial_runner.trial_runner_main.update_cumulative_metrics')
    @patch('trial_runner.trial_runner_main.run_adversarial_trial')
    def test_queues_updated_and_loop_triggered_multiple_times(self,mock_run_adversarial_trial,mock_update_cumulative_metrics):
        iteration_size = 5
        iteration_number = 3
        selected_attack = [None]
        selected_model = [None]
        hyperparameter_settings = [[]]
        image_queue = queue.Queue()
        graph_queue = queue.Queue()
        progress_bar_queue = queue.Queue()
        thread_killing_event = Event()
        back_end_main_loop(iteration_size,iteration_number,selected_attack,selected_model,hyperparameter_settings,image_queue,graph_queue,progress_bar_queue,thread_killing_event)
        self.assertEqual(image_queue.qsize(), 3)
        self.assertEqual(graph_queue.qsize(), 3)
        self.assertEqual(progress_bar_queue.qsize(), 3)
        self.assertEqual(mock_run_adversarial_trial.call_count,3)


    @patch('trial_runner.trial_runner_main.update_cumulative_metrics')
    @patch('trial_runner.trial_runner_main.run_adversarial_trial')
    def test_hyper_parameter_normal_parsing(self,mock_run_adversarial_trial,mock_update_cumulative_metrics):
        iteration_size = 5
        iteration_number = 3
        selected_attack = [None]
        selected_model = [None]
        hyperparameter_settings = [[1,2,3],[3,2,1]]
        image_queue = queue.Queue()
        graph_queue = queue.Queue()
        progress_bar_queue = queue.Queue()
        thread_killing_event = Event()
        back_end_main_loop(iteration_size,iteration_number,selected_attack,selected_model,hyperparameter_settings,image_queue,graph_queue,progress_bar_queue,thread_killing_event)
        expected_calls = [
            call(iteration_size,selected_attack,selected_model,[1,3],0),
            call(iteration_size,selected_attack,selected_model,[2,2],1),
            call(iteration_size,selected_attack,selected_model,[3,1],2)
        ]
        
        mock_run_adversarial_trial.assert_has_calls(expected_calls)

    @patch('trial_runner.trial_runner_main.update_cumulative_metrics')
    @patch('trial_runner.trial_runner_main.run_adversarial_trial')
    def test_hyper_parameter_empty_parsing(self,mock_run_adversarial_trial,mock_update_cumulative_metrics):
        iteration_size = 5
        iteration_number = 3
        selected_attack = [None]
        selected_model = [None]
        hyperparameter_settings = [[[None],[None],[None]],[[None],[None],[None]]]
        image_queue = queue.Queue()
        graph_queue = queue.Queue()
        progress_bar_queue = queue.Queue()
        thread_killing_event = Event()
        back_end_main_loop(iteration_size,iteration_number,selected_attack,selected_model,hyperparameter_settings,image_queue,graph_queue,progress_bar_queue,thread_killing_event)
        expected_calls = [
            call(iteration_size,selected_attack,selected_model,[[None],[None]],0),
            call(iteration_size,selected_attack,selected_model,[[None],[None]],1),
            call(iteration_size,selected_attack,selected_model,[[None],[None]],2)
        ]
        
        mock_run_adversarial_trial.assert_has_calls(expected_calls)


    @patch('trial_runner.trial_runner_main.update_cumulative_metrics')
    @patch('trial_runner.trial_runner_main.run_adversarial_trial')
    def test_hyper_parameter_repeat_parsing(self,mock_run_adversarial_trial,mock_update_cumulative_metrics):
        iteration_size = 5
        iteration_number = 4
        selected_attack = [None]
        selected_model = [None]
        hyperparameter_settings = [[1,2],[3,4]]
        image_queue = queue.Queue()
        graph_queue = queue.Queue()
        progress_bar_queue = queue.Queue()
        thread_killing_event = Event()
        back_end_main_loop(iteration_size,iteration_number,selected_attack,selected_model,hyperparameter_settings,image_queue,graph_queue,progress_bar_queue,thread_killing_event)
        expected_calls = [
            call(iteration_size,selected_attack,selected_model,[1,3],0),
            call(iteration_size,selected_attack,selected_model,[2,4],1),
            call(iteration_size,selected_attack,selected_model,[1,3],2),
            call(iteration_size,selected_attack,selected_model,[2,4],3)
        ]
        
        mock_run_adversarial_trial.assert_has_calls(expected_calls)


    @patch('trial_runner.trial_runner_main.update_cumulative_metrics')
    @patch('trial_runner.trial_runner_main.run_adversarial_trial')
    def test_results_directory_created_correctly(self,mock_run_adversarial_trial,mock_update_cumulative_metrics):
        iteration_size = 5
        iteration_number = 4
        selected_attack = [None]
        selected_model = [None]
        hyperparameter_settings = [[1,2],[3,4]]
        image_queue = queue.Queue()
        graph_queue = queue.Queue()
        progress_bar_queue = queue.Queue()
        thread_killing_event = Event()
        if os.path.exists('./results'):
            shutil.rmtree('./results')
        back_end_main_loop(iteration_size,iteration_number,selected_attack,selected_model,hyperparameter_settings,image_queue,graph_queue,progress_bar_queue,thread_killing_event)
        self.assertTrue(os.path.isfile('./results/cumulative_metrics.txt'))


    @patch('trial_runner.trial_runner_main.update_cumulative_metrics')
    @patch('trial_runner.trial_runner_main.run_adversarial_trial', side_effect=lambda  *args, **kwargs: (time.sleep(25)))
    def test_breaking_upon_event_setting(self,mock_run_adversarial_trial,mock_update_cumulative_metrics):
        iteration_size = 5
        iteration_number = 5
        selected_attack = [None]
        selected_model = [None]
        hyperparameter_settings = [[]]
        image_queue = queue.Queue()
        graph_queue = queue.Queue()
        progress_bar_queue = queue.Queue()
        thread_killing_event = Event()
        test_thread = threading.Thread(target = lambda: back_end_main_loop(iteration_size,iteration_number,selected_attack,selected_model,hyperparameter_settings,image_queue,graph_queue,progress_bar_queue,thread_killing_event))

        test_thread.start()

        time.sleep(0.5)

        thread_killing_event.set()

        test_thread.join()

        self.assertLess(mock_run_adversarial_trial.call_count,200)




if __name__ == '__main__':
    unittest.main()