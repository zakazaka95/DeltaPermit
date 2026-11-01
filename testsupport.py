"""Deterministic storage/consensus test double, NOT GenVM or an LLM benchmark."""
import copy
import importlib.util
import pathlib
import sys
import types


class UserError(Exception):
    pass


class Return:
    def __init__(self, calldata):
        self.calldata = calldata


class Runtime:
    def __init__(self):
        self.output = None
        self.validator_output = None
        self.mutate = None
        self.prompts = []
        self.calls = 0
        self.sender = "0x" + "1" * 40
        self.clock = 1_800_000_000
        self.fake = None

    def prompt(self, prompt, response_format=None):
        assert response_format == "json"
        self.prompts.append(prompt)
        self.calls += 1
        output = self.validator_output if self.calls % 2 == 0 and self.validator_output is not None else self.output
        if isinstance(output, Exception):
            raise output
        return copy.deepcopy(output)

    def run(self, leader, validator):
        candidate = leader()
        if self.mutate:
            candidate = self.mutate(copy.deepcopy(candidate))
        if not validator(Return(candidate)):
            raise AssertionError("Independent validator rejected the complete receipt")
        return candidate

    def as_sender(self, address):
        self.fake.message.sender_address = address
        self.sender = address


def load(filename="DeltaPermit.py"):
    runtime = Runtime()
    fake = types.ModuleType("genlayer")
    fake.contract = types.SimpleNamespace(Contract=object)
    fake.storage = types.SimpleNamespace(TreeMap=dict)
    fake.public = types.SimpleNamespace(write=lambda f: f, view=lambda f: f)
    fake.message = types.SimpleNamespace(sender_address=runtime.sender)
    fake.nondet = types.SimpleNamespace(exec_prompt=runtime.prompt)
    fake.vm = types.SimpleNamespace(UserError=UserError, Return=Return, run_nondet_default=runtime.run)
    types_module = types.ModuleType("genlayer.types")
    types_module.u64 = int
    types_module.__all__ = ["u64"]
    previous = {name: sys.modules.get(name) for name in ["genlayer", "genlayer.types"]}
    sys.modules["genlayer"] = fake
    sys.modules["genlayer.types"] = types_module
    path = pathlib.Path(__file__).with_name(filename)
    spec = importlib.util.spec_from_file_location(filename.removesuffix(".py"), path)
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    finally:
        for name, value in previous.items():
            if value is None:
                sys.modules.pop(name, None)
            else:
                sys.modules[name] = value
    runtime.fake = fake
    module._now = lambda: runtime.clock
    klass = getattr(module, filename.removesuffix(".py"))
    contract = klass()
    for name, annotation in klass.__annotations__.items():
        if getattr(annotation, "__origin__", None) is dict:
            setattr(contract, name, {})
    return module, contract, runtime
