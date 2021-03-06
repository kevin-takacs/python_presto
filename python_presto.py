#! /usr/bin/python
import sys
import optparse
import datetime
# Use the Python debugger to set an interactive trace.
"""
import pdb
pdb.set_trace()
"""
__program_name__ = "Python Presto"
__program_description__ = "A starting point for a Python program."
__file_name__ = "python_presto.py"
__author__ = "Kevin Takacs <kevin@kevin.pub>"
__copyright__ = "(C) 2015 GNU GPL 2"
__version__ = "1.0"
__credits__ = "www.python.org for the Option and OptionParser extensions."


class Stub:
    """ Describe the class here.
    """
    def __init__(self, test):
        """ The init method is called at the creation of a new class.  Arguments
        passed during the class creation are available to this method.
        """
        self.test = test
        return None


def stub():
    """ Describe the function here.
    """
    pass
    return None


class OptionsAndArguments():
    """ This class parses options and arguments passed from the command line in
    the common *NIX way (e.g. $ ./python_presto_v1.0.py --debug -e foo@bar.com
    logfile.txt).  In the example, the program is getting passed the debug
    option in the long format and the email option in the short format.  The
    argument 'logfile.txt' is also being passed.  Arguments are usually
    reserved for file handles that are going to be operated on, but don't have
    to be.
    """
    def __init__(self, option_definitions, program_name, program_description):
        """ On init, this class requires a list of tuples to be passed
        to it that define the options along with program information.
        """
        self.option_definitions = option_definitions
        self.program_name = program_name
        self.program_description = program_description
        self.option_list = self.get_option_list()
        self.usage_message = self.get_usage_message()
        self.options, self.arguments = self.get_options_and_arguments()
        return None

    def get_option_list(self):
        # Create the list of option objects based on the definitions.
        option_list = []
        for option_tuple in self.option_definitions:
            # Set arguments and keyword arguments from option_definitions.
            args = (option_tuple[0], option_tuple[1])
            kwargs = option_tuple[2]
            option_list.append(self.OptionParser.Option(*args, **kwargs))
        return option_list

    def get_usage_message(self):
        # Build usage message.
        usage_message = ""
        for option in self.option_list:
            usage_message += option._short_opts[0].replace("-", "")
        usage_message = "\n%s\n%s\n\n%s -[%s%s] " % (
            self.program_name,
            self.program_description,
            sys.argv[0],
            usage_message,
            "h"
        )
        return usage_message

    def get_options_and_arguments(self):
        # Parse the list of options and assign values to the attributes.
        option_parser = self.OptionParser(
            usage=self.usage_message,
            option_list=self.option_list
        )
        return option_parser.parse_args()

    class OptionParser(optparse.OptionParser):
        """ Taken from python.org.  OptionParser extends optparse.OptionParser.
        """
        class Option(optparse.Option):
            """Taken from python.org.  Extend 'optparse.Option' object to
            account for required options.
            """
            ATTRS = optparse.Option.ATTRS + ['required']

            def _check_required(self):
                if self.required and not self.takes_value():
                    raise OptionError(
                        """Required flag set for option that doesn't take
                        a value
                        """,
                        self
                    )
                return None
            # Make sure _check_required() is called from the constructor.
            CHECK_METHODS = optparse.Option.CHECK_METHODS + [_check_required]

            def process(self, opt, value, values, parser):
                optparse.Option.process(self, opt, value, values, parser)
                parser.option_seen[self] = 1
                return None

        def _init_parsing_state(self):
            optparse.OptionParser._init_parsing_state(self)
            self.option_seen = {}
            return None

        def check_values(self, values, args):
            for option in self.option_list:
                if isinstance(option, self.Option) and \
                option.required and not \
                self.option_seen.has_key(option):
                    self.error("%s not supplied" % option)
            return (values, args)


def print_red(text, center=False):
    if center:
        space = " " * int((80 - len(text)) / 2)
        text = "%s%s%s" % (space, text, space)
        if not len(text) == 80:
            text += " " * (80 - len(text))
    code_red = "\x1b[1m\x1b[37m\x1b[41m"
    code_black = "\x1b[22m\x1b[39m\x1b[49m"
    text = "%s%s%s" % (code_red, text, code_black)
    print text
    return None


def now_stamp():
    """ Returns a the datetime of now in the format YYMMDD_HHMMSS.
    """
    return datetime.datetime.now().strftime("%y%m%d_%H%M%S")


def file_to_string(filepath):
    """ Read in a file and return it as a string.
    """
    try:
        return open(filepath, 'r').read()
    except IOError:
        exit("IOError Exception: FILE NOT FOUND")
    return None


def file_to_list(filepath):
    """ Read in a file and return it as a list with each line as an element.
    """
    try:
        lines = [
            line.replace('\n', '')
            for line in open(filepath, 'r').readlines() if line
        ]
        return lines
    except IOError:
        exit("IOError Exception: FILE NOT FOUND")
    return None


def list_to_print(list):
    """ Print a passed list.
    """
    for line in list:
        print line
    return None


def dict_to_print(d):
    """ Print a passed dictionary.
    """
    for key in d.keys():
        spaces = " " * (10 - len(key))
        print "key:%s %s value:%s" % (key, spaces, d[key])
    return None


def main():
    # Set-up options and arguments. Example:
    option_definitions = [
        ('-r', '--red', {'action': 'count'}),
        ('-a', '--animal', {'required': 0}),
    ]
    args = [option_definitions, __program_name__, __program_description__]
    cli = OptionsAndArguments(*args)
    # Examples of option and argument methods and properties:
    """
    print cli.options.animal
    print cli.options.red
    """
    # A list of animals:
    animals = ['turkey', 'donkey', 'monkey', 'horsey']
    # Add an animal if passed from CLI.
    if cli.options.animal:
        animals.append(cli.options.animal)
    """ A list comprehension example to only return animals with the string
    'key' in their names and to also make the names upper case.
    """
    animals = [animal.upper() for animal in animals if 'key' in animal]
    # An enumerate and print format example.
    for count, animal in enumerate(animals):
        if cli.options.red:
            print_red("%s - HELLO %s FACE! It's %s" % (
                count, animal, now_stamp()), center=True
            )
        else:
            print "%s - HELLO %s FACE! It's %s" % (count, animal, now_stamp())
    return None


if __name__ == '__main__':
    main()

