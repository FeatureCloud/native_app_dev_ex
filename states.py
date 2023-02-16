from FeatureCloud.app.engine.app import AppState, app_state, Role
import pandas as pd
import numpy as np


@app_state('initial')
class InitialState(AppState):

    def register(self):
        self.register_transition('write_res', Role.PARTICIPANT)
        self.register_transition('global_agg', Role.COORDINATOR)

    def run(self):
        # read_data
        df = pd.read_csv("mnt/input/counts.tsv", sep='\t')

        # get local mean and var
        local_mean = df.mean()
        local_var = df.var()
        self.send_data_to_coordinator(data=[local_mean, local_var])
        if self.is_coordinator:
            return 'global_agg'
        return 'write_res'


@app_state('global_agg', role=Role.COORDINATOR)
class GlobalAgg(AppState):

    def register(self):
        self.register_transition('write_res', role=Role.COORDINATOR)

    def run(self):
        received_data = self.gather_data()
        global_mean, global_var = np.mean(received_data, axis=0)
        self.broadcast_data(data=[global_mean, global_var])

        return 'write_res'


@app_state('write_res')
class WriteRes(AppState):

    def register(self):
        self.register_transition('terminal')

    def run(self):
        global_mean, global_var = self.await_data()
        self.log(f"Mean: {global_mean}, Var: {global_var}")
        return 'terminal'
