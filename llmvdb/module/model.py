# Load model directly
from transformers import AutoTokenizer, GPTNeoXModel, GPTNeoXConfig
import torch
from typing import Optional


class Model:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("beomi/KoAlpaca-Polyglot-5.8B")
        self.model = InputEmbeddingModel.from_pretrained("beomi/KoAlpaca-Polyglot-5.8B")

    def get_embedding(self, prompt):
        inputs = self.tokenizer(prompt, return_tensors="pt")
        embedding = self.model(inputs.input_ids)  # ['last_hidden_state']

        # Calculate the sentence vector by averaging the hidden states across the sequence length dimension
        sentence_vector = torch.mean(embedding, dim=1)

        print(prompt)

        return sentence_vector


class InputEmbeddingModel(GPTNeoXModel):
    def __init__(self, config: GPTNeoXConfig):
        super().__init__(config)

    def forward(
        self,
        input_ids: Optional[torch.LongTensor] = None,
        inputs_embeds: Optional[torch.FloatTensor] = None,
    ):
        if inputs_embeds is None:
            inputs_embeds = self.embed_in(input_ids)

        return inputs_embeds