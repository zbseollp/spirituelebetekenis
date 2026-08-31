export const site = {
  name: "Spirituele Betekenissen",
  domain: "https://spirituelebetekenis.com",
  titleSuffix: " - Spirituele Betekenissen",
  logo: "/wp-content/uploads/2023/04/logo-spirituelebetekenis.com_.png",
  description:
    "Laat je leiden door de kracht van intuïtie en spiritualiteit. Ontdek de spirituele betekenis achter getallen, sterrenbeelden, dieren en tekens.",
};

// Exact het menu van de oude site: "Blog" is een dropdown zonder eigen pagina.
export const nav = [
  { label: "Home", href: "/" },
  { label: "Trainingen", href: "/trainingen/" },
  {
    label: "Blog",
    href: "#",
    children: [
      { label: "Alle Berichten", href: "/blog/" },
      { label: "Astrologie", href: "/info/astrologie/" },
      { label: "Numerologie", href: "/info/numerologie/" },
      { label: "Spiritualiteit", href: "/info/spiritualiteit/" },
      { label: "Spirituele Betekenissen", href: "/info/spirituele-betekenissen/" },
      { label: "Sterrenbeelden", href: "/info/sterrenbeelden/" },
    ],
  },
  { label: "Contact", href: "/contact/" },
];

/**
 * De affiliate-links van de oude site zijn gemaskeerde redirects
 * (/bol, /intuitie, ...). De redirect-plugin die dat deed is stuk: op de live
 * site geven ze op dit moment allemaal een 404.
 *
 * De doelen staan in affiliate-redirects.json, dat ook de Worker inleest. Vul
 * daar de echte affiliate-URL in en de Worker stuurt de bezoeker door met een
 * 301. Zolang een doel leeg is gedraagt het pad zich als nu op de oude site.
 */
import redirects from "./affiliate-redirects.json";
export const affiliateRedirects: Record<string, string> = redirects;

export const sidebarPromos = [
  {
    title: "Duizenden spirituele producten op bol.com",
    image: "/wp-content/uploads/2023/12/PNG-Bol-icon.png",
    href: "/bol",
    button: "Meer info",
    text: "",
  },
  {
    title: "Tekens Zijn Overal",
    image: "/wp-content/uploads/2023/12/tekens-zijn-overal-1.jpg",
    href: "/tekenszijnoveral",
    button: "Meer info",
    text: "",
  },
  {
    title: "Het Leven dat Jou Past",
    image: "/wp-content/uploads/2023/12/het-leven-dat-jou-past.jpg",
    href: "/hetlevendatjoupast",
    button: "Meer info",
    text: "",
  },
  {
    title: "How To Be The Love You Seek",
    image: "/wp-content/uploads/2023/12/how-to-be-the-love-you-seek.jpg",
    href: "/howtobetheloveyouseek",
    button: "Meer info",
    text: "",
  },
  {
    title: "Training Manifesteren",
    image: "/wp-content/uploads/2024/03/training-manifesteren.jpg",
    href: "/trainingmanifesteren",
    button: "Bekijk training",
    text: "Laat dromen en verlangens werkelijkheid worden",
  },
  {
    title: "Training Intuïtie",
    image: "/wp-content/uploads/2024/03/training-intuitie.jpg",
    href: "/intuitie",
    button: "Bekijk training",
    text: "Kom in contact met je zesde zintuig",
  },
  {
    title: "Mindful Leven",
    image: "/wp-content/uploads/2024/03/training-mindful-leven.jpg",
    href: "/mindfulleven",
    button: "Bekijk training",
    text: "Leer ontspannen in het hier en nu met mindfulness",
  },
];

export const contact = {
  email: "info@spirituelebetekenis.com",
  address: ["Tinhoutstraat 145", "8730 Oedelem"],
  // Het contactformulier loopt via Web3Forms, met dezelfde access key als de
  // andere sites; die bepaalt naar welk mailadres het bericht gaat. Maak hem
  // leeg en /contact/ toont het mailadres in plaats van een formulier.
  web3formsKey: "281f477d-7744-407d-9b6a-9b8d9c6abe3c",
};

export const POSTS_PER_PAGE = 40; // zoals de oude site
