import { Typography, useTheme, Accordion, AccordionSummary, AccordionDetails } from "@mui/material";
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import { Box } from "@mui/material";
import { tokens } from "../../theme";

const Faq = () => {
    const theme = useTheme();
    const colors = tokens(theme.palette.mode);

    const faqData = [
        {
            question: "How are the options ranked?",
            answer: "Options are ranked by the maximum gain/loss possible, for both the buy side and sell side. Gain/loss is calculated by getting the highest high and lowest low it has ever been."
        },
        {
            question: "How does the expectation chart work?",
            answer: `The projections are calculated by offsetting the pricing of
            call and put option contracts against each other, taking into account
            of interest rate and implied volatility, how much of a difference of pricing
            are there between the contracts with same $ distance`
        },
        {   question: "What is the purpose of this project?",
            answer: `The purpose is to try and create a hawkeye view on the market implied by
            the options traded, simplifying complex information. Second reason is to practice building a fully functional web from start to finish`
        },

        // ... other FAQ items
    ];

    return (
        <Box
            height="90vh"
            sx={{
                color: colors.grey[100],
                overflow: 'auto', // in case of scrolling
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center', // centers the accordion horizontally
            }}
        >
            <Box margin="5vh" textAlign="center">
                <Typography variant="h2" fontWeight="bold" gutterBottom>
                    Frequently Asked Questions
                </Typography>
            </Box>

            {faqData.map((faq, index) => (
                <Accordion key={index} sx={{ maxWidth: '800px', width: '100%', marginBottom: '1vh' }}>
                    <AccordionSummary
                        expandIcon={<ExpandMoreIcon />}
                        aria-controls={`panel${index}a-content`}
                        id={`panel${index}a-header`}
                        sx={{ backgroundColor: colors.grey[800], borderRadius: '4px' }} // Add styling as needed
                    >
                        <Typography variant="h5" sx={{ fontSize: '1.25rem' }}>{faq.question}</Typography>
                    </AccordionSummary>
                    <AccordionDetails sx={{ backgroundColor: colors.grey[700] }}>
                        <Typography variant="body1">{faq.answer}</Typography>
                    </AccordionDetails>
                </Accordion>
            ))}

            {/* Add more FAQs as needed */}
        </Box>
    );
}

export default Faq;
