import json
from . import DecodingExperiment

class CssDecodingExperiment(DecodingExperiment):
    def __init__(self, code, x_decoder, z_decoder, noise):
        self.code = code
        self.x_decoder = x_decoder 
        self.z_decoder = z_decoder 
        self.noise = noise

    def run_once(self):
        """ Runs a random decoding simulation and returns True if the process
        is successful. Else returns False.
        """
        error = self.noise.sample_error_of_length(len(self.code))
        (x_syndrome, z_syndrome) = self.code.syndrome_of(error)
        x_correction = self.x_decoder.decode(x_syndrome)
        z_correction = self.z_decoder.decode(z_syndrome)
        return self.code.has_stabilizer(x_correction.apply(z_correction).apply(error))

    def to_json(self):
        return json.dumps(
            {
                "length": len(self.code),
                "dimension": self.code.dimension(),
                "num_x_stabs": self.code.num_x_stabs(),
                "num_z_stabs": self.code.num_z_stabs(),
                "x_decoder": self.x_decoder.to_json(),
                "z_decoder": self.z_decoder.to_json(),
            }
        )

    def error_probability(self):
        return self.noise.error_probability()

    def tag(self):
        try:
            code_tag = self.code.tag()
        except:
            code_tag = None
        try:
            decoder_tag = self.x_decoder.tag() + " / " + self.z_decoder.tag()
        except:
            decoder_tag = None

        if code_tag and decoder_tag:
            return f"{code_tag} + {decoder_tag}"
        elif code_tag:
            return code_tag
        elif decoder_tag:
            return decoder_tag
        else:
            return ""
