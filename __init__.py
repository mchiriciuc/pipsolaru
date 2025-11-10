import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import uart
from esphome.const import CONF_ID

DEPENDENCIES = ["uart"]
CODEOWNERS = ["@andreashergert1984"]
AUTO_LOAD = ["binary_sensor", "text_sensor", "sensor", "switch", "output", "select"]
MULTI_CONF = True

CONF_PIPSOLAR_ID = "pipsolar_id"
CONF_DUAL_MPPT = "dual_mppt"

pipsolar_ns = cg.esphome_ns.namespace("pipsolar")
PipsolarComponent = pipsolar_ns.class_("Pipsolar", cg.Component)

PIPSOLAR_COMPONENT_SCHEMA = cv.Schema(
    {
        cv.Required(CONF_PIPSOLAR_ID): cv.use_id(PipsolarComponent),
    }
)

CONFIG_SCHEMA = cv.All(
    cv.Schema({
        cv.GenerateID(): cv.declare_id(PipsolarComponent),
        cv.Optional(CONF_DUAL_MPPT, default=False): cv.boolean,
    })
    .extend(cv.polling_component_schema("1s"))
    .extend(uart.UART_DEVICE_SCHEMA)
)


def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    yield cg.register_component(var, config)
    yield uart.register_uart_device(var, config)
    
    # Set dual_mppt flag
    cg.add(var.set_dual_mppt(config[CONF_DUAL_MPPT]))
